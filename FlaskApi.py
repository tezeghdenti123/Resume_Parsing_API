from flask import Flask,request,jsonify
from Services.Service import Service
from Models.Consultant import Consultant
import os

app=Flask(__name__)
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/")
def home():
    return "Home"


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
        email=Service.extractEmailFromText(text)
        phoneNumber=Service.extract_phone_number(text)
        linkedIn=Service.extract_linkedin_url(text)
        languages=Service.extract_language(text)
        service=Service()
        skillsList=service.extract_skills(text)
        consultant=Consultant("",email ,linkedIn,phoneNumber,languages,skillsList)
        return jsonify(consultant.__dict__)

    return jsonify({'error': 'Invalid file format. Please upload a PDF file'})



if __name__ == "__main__":
    app.run(debug=True)





