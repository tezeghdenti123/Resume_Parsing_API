from flask import Flask,request,jsonify
import os
from flask_cors import CORS
from flask_mysqldb import MySQL
import threading
from Services.ScrapingService import ScrapingService
from flair.models import SequenceTagger
import nltk
from nltk.corpus import stopwords
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def createApp():
    app=app=Flask(__name__)
    CORS(app)  # This will enable CORS for all routes

    UPLOAD_FOLDER = 'static/files'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = ':///User.mysql'
    return app

def createMysqlInstance(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Mohamed2019$'
    app.config['MYSQL_DB'] = 'crudapi'

    return MySQL(app)

def startScrapingTask(mysql,app):
    try:
        service=ScrapingService()
        
        scheduler = BackgroundScheduler()
        if not scheduler.running:
        # Schedule the job to run every day at 8:00 AM
            scheduler.add_job(service.getCleanedOpportunityList, 'interval', minutes=1,args=[mysql,app])

        # Start the scheduler
            scheduler.start()
        
    except Exception as e:
        print("SchedulerException: Job interupted!")


def getTagger():
    return SequenceTagger.load("flair/ner-french")
