from flask import Flask,request,jsonify
from Services.ScrapingService import ScrapingService
from Services.ResumeParserService import Service
from Services.MySqlService import MySqlService
from Services.RecommendationService import RecommendationService
from Services.StatisticService import StatisticService
from flair.models import SequenceTagger
from Services.CandidateDBService import CandidateDBService
from Services.CandidateRecommendationService import CandidateRecommendationService
from werkzeug.utils import secure_filename
import nltk
from nltk.corpus import stopwords
from app import createApp,createMysqlInstanceScrapping,startScrapingTask,getTagger
import threading
from io import BytesIO
import logging
import tempfile
from ultralytics import YOLO
from pdf2image import convert_from_path
from paddleocr import PaddleOCR, draw_ocr
import os


app=createApp()
mysql=createMysqlInstanceScrapping(app)
nltk.download('stopwords')
nltk.download('punkt')
tagger=SequenceTagger.load("flair/ner-french")
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to best5.pt
model_path = os.path.join(base_dir, 'best5.pt')
# Load the YOLO model
model = YOLO(model_path)

# Initialize the PaddleOCR reader
ocr = PaddleOCR(use_angle_cls=True, lang='en')
@app.route("/")
def home():
    return "Home"

# Flag to track whether the endpoint has been invoked
endpoint_invoked = False

@app.route('/invokeOnce', methods=['GET'])
def invoke_once():
    global endpoint_invoked
    if not endpoint_invoked:
        # Your logic for the endpoint goes here
        # For example, you can return a message indicating success
        startScrapingTask(mysql,app)
        num_threads = threading.active_count()

        print("Number of active threads:", num_threads)
        endpoint_invoked = True
        return 'Scraper invoked successfully', 200
    else:
        # If the endpoint has already been invoked, return an error message
        return 'Endpoint already invoked', 400




@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the POST request has a file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Check if the file is a PDF
    if file and file.filename.endswith('.pdf'):
        # Perform actions with the PDF file, e.g., save it or process it
        # In this example, we'll just return a success message
        
        file_path=Service.saveFile(file,app.config['UPLOAD_FOLDER'])
        
        text=Service.extract_content(file_path)
        consultant=Service.ResumeToConsultant(text,tagger)
        return jsonify(consultant.__dict__)

    return jsonify({'error': 'Invalid file format. Please upload a PDF file'})

@app.route('/scraper', methods=['POST'])
def scraper():
    scrapingService=ScrapingService()
    return scrapingService.getCleanedOpportunityList(mysql,app)

@app.route('/test', methods=['GET'])
def test():
    mysqlService=MySqlService()
    #data= mysqlService.getAllOpportunity(mysql)
    #data=mysqlService.saveOpportunity(mysql,"test","test","test","test","test","test")
    #data=mysqlService.deleteAllOpportunity(mysql)
    recommendationService=RecommendationService()
    data=recommendationService.getOpportunityList(mysql)
    return str(data)

@app.route('/statistic', methods=['GET'])
def getStatistic():
    
    statisticService=StatisticService()
    data=statisticService.getStatistic(mysql)
    return data

@app.route('/recommendation', methods=['POST'])
def getRecommendations():
    if request.method == 'POST':
        # Assuming the object is sent as JSON data
        consultant = request.json
        recommendationService=RecommendationService()
        data=recommendationService.getRecommendationOpportunity(mysql,consultant)
        # Process the received object as needed
        # For example, you can access its fields like data['field_name']
        
        # Return a response (optional)
        return data, 200
    else:
        return jsonify({'error': 'Method not allowed'}), 405



@app.route('/saveCandidate', methods=['POST'])
def save_candidate():
    # Get the JSON data from the request
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    title=request.form.get('title')
    offreId=int(request.form.get('offreId'))
    cover_letter = request.form.get('coverLetter')
    cv_file = request.files.get('cvFile')
    
    if not all([name, email, phone, cover_letter, cv_file]):
        return jsonify({"error": "Missing required fields"}), 400

    
    candidateDBService=CandidateDBService()
    
    # Insert the candidate profile into the collection
    result = candidateDBService.store_candidate_profile(name,email,phone,title,cover_letter,offreId,cv_file)
    '''return jsonify({"message": "Candidate profile saved", "id": str(result.inserted_id)}), 201'''
    return jsonify({"message": "Candidate profile saved"}), 201


@app.route('/getCandidates', methods=['GET'])
def get_candidates():
    # Get the optional offre_id parameter
    offre_id = request.args.get('offreId')
    candidateDBService=CandidateDBService()
    candidateRecommendationService=CandidateRecommendationService()
    # If offre_id is provided, filter by it
    if offre_id:
        candidates_list =candidateDBService.get_candidate_profile(int(offre_id))
        #return jsonify(candidates_list), 200
        text=candidateRecommendationService.candidateListToDataFrame(candidates_list,tagger)
        return str(text), 200
    
    if not candidates_list:
        return jsonify({"error": "No candidates found"}), 404

    return jsonify(candidates_list), 200
    
@app.route('/getCandidatesRec', methods=['GET'])
def get_candidates_rec():
    # Get the optional offre_id parameter
    offre= request.get_json()

    candidateDBService=CandidateDBService()
    candidateRecommendationService=CandidateRecommendationService()
    # If offre_id is provided, filter by it
    text=candidateRecommendationService.getRecommendationOpportunity(offre,tagger)
    
   
    return str(text), 200

    

@app.route('/test', methods=['POST'])
def Test():
    if request.method == 'POST':
        # Assuming the object is sent as JSON data
        statisticService=StatisticService()
        statisticService.Test(mysql)
        return "Ok",200
    else:
        return jsonify({'error': 'Method not allowed'}), 405


if __name__ == "__main__":

    app.run(debug=True)





