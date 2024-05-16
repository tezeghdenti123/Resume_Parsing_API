from flask import Flask,request,jsonify
from Services.ScrapingService import ScrapingService
from Services.ResumeParserService import Service
from Services.MySqlService import MySqlService
from Services.RecommendationService import RecommendationService
from flair.models import SequenceTagger
from werkzeug.utils import secure_filename
import nltk
from nltk.corpus import stopwords
from app import createApp,createMysqlInstance,startScrapingTask,getTagger
import threading

app=createApp()
mysql=createMysqlInstance(app)
nltk.download('stopwords')
nltk.download('punkt')
tagger=SequenceTagger.load("flair/ner-french")

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
        return 'Endpoint invoked successfully', 200
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

if __name__ == "__main__":

    app.run(debug=True)





