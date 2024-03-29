import fitz  # PyMuPDF
import re
import os
import spacy
from flair.data import Sentence
from flair.models import SequenceTagger
from werkzeug.utils import secure_filename
import nltk
from nltk.corpus import stopwords
from Models.Consultant import Consultant


class Service:
    
        
        
    def extract_content(file_path):
        cvfile = fitz.open(file_path)
        text=""
        nbPage=cvfile.pageCount
        for i in range(nbPage):
            page=cvfile.loadPage(i)
            text+=page.getText('text')
        return text
    
    def saveFile(file ,upload_folder):
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        file_path = os.path.join(upload_folder, filename)
        return file_path
    
    def remove_stopwords_french(self,text):
        stop_words = set(stopwords.words('french'))
        words = nltk.word_tokenize(text)
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return ' '.join(filtered_words)

    def remove_punctuation_and_special_chars_and_numbers(self,text):
        # Using regular expression to remove all non-alphanumeric characters
        text_without_chars = re.sub(r'[^A-Za-zéàÇ\s]', '', text)
        
        return text_without_chars

    def extractEmailFromText(text):
        pattern = re.compile(r'[^\s\n]+@[a-zA-Z-]+\.[a-zA-Z]{2,}')
        matches = re.findall(pattern, text)
        return matches

    def extract_language(text):
        listLanguage=[]
        arabe_pattern = re.compile(r'[aA][rR][aA][bB][eE]')
        matches = re.findall(arabe_pattern, text)
        listLanguage.append(matches)
        french_pattern = re.compile(r'[fF][rR][aA][nN][cCç][aA][iI][sS]|[fF][rR][eE][nN][cC][hH]')
        matches = re.findall(french_pattern, text)
        listLanguage.append(matches)
        english_pattern = re.compile(r'[aA][nN][gG][lL][aA][iI][sS]|[eE][nN][gG][lL][iI][sS][hH]')
        matches = re.findall(english_pattern, text)
        listLanguage.append(matches)
        deutsh_pattern = re.compile(r'[aA][lL][lL][eE][mM][aA][nN][dD]|[dD][eE][uU][tT][sS][cC][hH]')
        matches = re.findall(deutsh_pattern, text)
        listLanguage.append(matches)
        
        return listLanguage

    def extract_linkedin_url(text):
        linkedin_pattern = re.compile(r'https://www.linkedin\.com/in/[^ \n]*|linkedin\.com/in/[^ \n]*')
        matches = linkedin_pattern.findall(text)
        
        if matches:
            return matches[0]
        else:
            return None
        
    def extract_phone_number(text):
        phone_number_pattern = re.compile(r'[+(]?[0-9][+(.)\- ]?[0-9][+(.)\- ]?[0-9][+(.)\- ]?[0-9][+(.)\- ]?[0-9][+(.)\- ]?[0-9][+(.)\- ]?[0-9][+(.)\- ]?[0-9][+(.)\- ]?[0-9][^a-zA-Z\n]*')
        matches = phone_number_pattern.findall(text)
        
        if matches:
            return matches
        else:
            return None
    

    def extract_skills(self,text):
        textWithoutStopWords=self.remove_stopwords_french(text)
        #text=remove_punctuation_and_special_chars_and_numbers(text)
        #print(text)

        lowerText=textWithoutStopWords.lower()
        lowerwords=lowerText.split()
        combinedWords=[]
        #print(words)
        #here we will read all the skills from the skillsdataset file and put them in a list
        
        with open('/home/mohamedtez/Desktop/CVAPI/Services/SkillsDataSet', 'r+') as file:
            # Read the entire content of the file
            content = file.read()
            predefinedSkills=content.split('\n')
            #print(skillWords)
        
        predefinedSkills=self.getSkillsFromDataBase()
        #here we will iterate throw out the list of word and make all the possible combinition of two words to capter the combine skill like "react native"
        for i in range(len(lowerwords)-1):
            combinedWords.append(lowerwords[i]+" "+lowerwords[i+1])
        #print(combinedWords)

        lowerwords=lowerwords+combinedWords
        ##print(words)
        ##here from words we want to extract the skills
        skills=[]
        for word in lowerwords:
            if word in predefinedSkills:
                skills.append(word)

        return list(set(skills))
    def getSkillsFromDataBase(self):
        
        with open('/home/mohamedtez/Desktop/CVAPI/Services/SkillsDataSet', 'r+') as file:
            # Read the entire content of the file
            content = file.read()
            skillWords=content.split('\n')
            #print(skillWords)
        return skillWords
    

    def ResumeToConsultant(text,tagger):
        email=Service.extractEmailFromText(text)
        if(email!=None)and(len(email)>0):
            email=email[0]
        phoneNumber=Service.extract_phone_number(text)
        if(phoneNumber!=None):
            phoneNumber=phoneNumber[0]
        linkedIn=Service.extract_linkedin_url(text)
        if(linkedIn!=None):
            linkedIn=linkedIn[0]
        languages=Service.extract_language(text)
        langList=[]
        for langue in languages:
            if(len(langue)!=0):
                langList.append(langue[0])
        languages=langList
        service=Service()
        skillsList=service.extract_skills(text)
        name=service.extract_name(text,tagger)
        consultant=Consultant(name,email ,linkedIn,phoneNumber,languages,skillsList)
        return consultant
    
    def contains_only_alphabetic_and_spaces(self,sentence):
        return all(char.isalpha() or char == '.' or char.isspace() for char in sentence)


    def is_Valid_words(self,text):
        if(self.contains_only_alphabetic_and_spaces(text)==False):
            return False
        stop_words = set(stopwords.words('french'))
        words = nltk.word_tokenize(text)
        for word in words:
            if word.lower() in stop_words:
                return False
        
        return True
    
    


    def extract_name(self,text,tagger):
        
        sentenceList=text.split('\n')
        listWords=[]
        for sentence in sentenceList:
            sentence = ' '.join(sentence.split())
            if(0<len(sentence.split())<=3)and(self.is_Valid_words(sentence)==True):
                listWords.append(sentence)
        print(listWords)
        name=""
        if('Docker' in listWords):
            listWords.remove('Docker')
        
        if('French' in listWords):
            listWords.remove('French')
        max=0
        for sentence in listWords:
            sentence = Sentence(sentence)
            tagger.predict(sentence)
            for entity in sentence.get_spans('ner'):
                if(entity.tag=="PER")and(entity.score>max):
                    name=entity.text
                    max=entity.score
                    print(entity)

        print(name)
        return name