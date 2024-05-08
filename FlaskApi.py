from flask import Flask,request,jsonify
from flask_cors import CORS

from Services.Service import Service
from Models.Consultant import Consultant
import os
from flair.data import Sentence
from flair.models import SequenceTagger
from werkzeug.utils import secure_filename
import nltk
from nltk.corpus import stopwords
from Models.Consultant import Consultant
from pdfminer.high_level import extract_pages,extract_text
from docx import Document
import re

app=Flask(__name__)
CORS(app)  # This will enable CORS for all routes

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/")
def home():
    return "Home"

tagger = SequenceTagger.load("flair/ner-french")
nltk.download('stopwords')
nltk.download('punkt')

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



if __name__ == "__main__":
    app.run(debug=True)





