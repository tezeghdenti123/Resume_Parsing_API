from pymongo import MongoClient
import gridfs
from bson import ObjectId

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['candidate_profiles']

# Create a GridFS instance
fs = gridfs.GridFS(db)

class CandidateDBService:

    def store_candidate_profile(self,name, email, phone,title, cover_letter,offreId, cv_file):
        # Read the CV file
        cv_file_id = fs.put(cv_file, filename=cv_file.filename)

        # Create the candidate profile document
        candidate_profile = {
            "name": name,
            "email": email,
            "phone": phone,
            "title":title,
            "cover_letter": cover_letter,
            "offre_id":offreId,
            "cv_file_id": cv_file_id
        }

        # Insert the candidate profile into the collection
        result = db.profiles.insert_one(candidate_profile)
        print(f"Inserted candidate profile with ID: {result.inserted_id}")



    def get_candidate_profile(self,offre_id):
        candidates = db.profiles.find({ "offre_id": offre_id })
        candidates_list = []
        for candidate in candidates:
            candidate['_id'] = str(candidate['_id'])  # Convert ObjectId to string
            cv_file_id=candidate['cv_file_id']
            candidate['cv_file_id'] = str(candidate['cv_file_id'])  # Convert ObjectId to string
            candidate['cv_file'] = fs.get(cv_file_id)
            #candidate['cv_file'] = cv_file
            '''cv_file_path = "retrieved_cv.pdf"
            with open(cv_file_path, 'wb') as file:
                file.write(cv_file.read())
                print(f"CV saved to {cv_file_path}")'''
            candidates_list.append(candidate)
        return candidates_list