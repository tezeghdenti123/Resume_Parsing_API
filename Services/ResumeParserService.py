import re
import os
import spacy
from flair.data import Sentence
from flair.models import SequenceTagger
from werkzeug.utils import secure_filename
import nltk
from nltk.corpus import stopwords
from Models.Consultant import Consultant
from pdfminer.high_level import extract_pages,extract_text


class Service:
    
        
        
    def extract_content(file_path):
        #cvfile = fitz.open(file_path)
        #text=""
        #nbPage=cvfile.pageCount
        text=extract_text(file_path)

        #for i in range(nbPage):
        #    page=cvfile.loadPage(i)
        #    text+=page.getText('text')
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
        
        with open('/home/tezeghdentimohamed/Desktop/CVAPI/Services/SkillsDataSet', 'r+') as file:
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
        
        with open('/home/tezeghdentimohamed/Desktop/CVAPI/Services/SkillsDataSet', 'r+') as file:
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
        educationList=service.getListEduOrg(text)
        consultant=Consultant(name,email ,linkedIn,phoneNumber,languages,skillsList,educationList,[])
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
    
    def is_empty_or_spaces(self,sentence):
        return len(sentence.strip()) == 0

    def isdate(self,sentence):
        pattern1 = re.compile(r'[1][9][0-9][0-9]|[2][0][0-9][0-9]')
        matches1 = re.findall(pattern1, sentence)
        return matches1
    def isdate(self,sentence):
        pattern1 = re.compile(r'[1][9][0-9][0-9]|[2][0][0-9][0-9]')
        matches1 = re.findall(pattern1, sentence)
        return matches1

    def isDiplomat(self,sentence):
        pattern1 = re.compile(r'BUT[^a-zA-Z]|L2|L1|IUP|DESS|LPIC|Certiﬁcat:|C[eE][rR][tT][iI][fF][iI][cC][aA][tT][^a-zA-Z]|(?:^|[^A-Za-z])Formation[\s](?!et|d[eu]|[cC][lL][iI][eE][nN][tT]|\W*$)|System and Information Technology|PMP|[gG][rR][aA][dD][uU][tT][eE]|1 ère année|Ingénieurie|[Ss]oftware [eE]ngineer|[Cc][Yy][cC][lL][eE][\s][dDiI]|[cC][eE][rR][tT][iI][fF][iI][cC][Aa][Tt][eE]?[^a-zA-Z]|[Pp][rR][Ee][pP][aA][rR][aA][tT][oO][rR][Yy]|[^tT][\s][Pp][rR][eEéÉ][pP][aA][rR][aA][tT][oO][iI][rR]|B[\.\s]?[sS][\.\s]?[Cc][^a-zA-Z]|[pP][\.\s]?[hH][\.\s]?[dD]|[Dd][eE][gG][Rr][Ii][eE]|[Cc][Pp][gG][Ee]|[mM][aA][iIî][tT][rR][iI][sS][eE][\s][^dD]|[Bb][tT][sS]|[lL][iI][cC][eE][Nn][cCsS][eE]|MS[cC]|(?:^|[^A-Za-z])[mM][aA][sS][tT][eEèÈ][rR]|[dD][iI][pP][lL][oOô][mM][eE][\s]|[dD][iI][pP][lL][oOô][mM][aA]|[Bb][aA][cC][^a-zA-Z]|[Bb][aA][cC][^kKhH][^Oo]|[bB][aA][Cc][Hh][Ee][Ll][oO]|[iI][nN][gG][eÉEé][nN][iI][eE][rR][iI][eE][\s][eE][nN]|[Dd][uU][tT][\s]|[^a-zA-Z]?B\.?E[^a-zA-Z]|[Aa][sS][sS][oO][cC][iI][aA][tT][eE]|[Dd][oO][cC][tT][oO][rR]|M[\s\.]2') # DUT BTS master formation licence cycl cert bac diplome genie BE associat doctor 
        matches1 = re.findall(pattern1, sentence)
        return matches1

    def remove_punctuation_and_special_chars_and_numbers(self,text):
        # Using regular expression to remove all non-alphanumeric characters
        text_without_chars = re.sub(r'[^A-Za-zéàÇ\s]', '', text)
        
        return text_without_chars

    def extract_text_from_docx(docx_path):
        doc = Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    def remove_punctuation_and_special_chars_and_numbers(text):
        # Using regular expression to remove all non-alphanumeric characters
        text_without_chars = re.sub(r'[^A-Za-zéàÇ\s]', '', text)
        
        return text_without_chars

    
    
    def getTypleOfExperienceAndEducation(self,listOfsentences):
        expBloc=False #it is active if the bloc is Experience bloc
        eduBloc=False #it is active if it is an Education bloc
        certBloc=False
        listExperience=[]
        listEducation=[]
        for sentence in listOfsentences:

            pattern = re.compile(r'E[\s]?[xX][\s]?[pP][\s]?[eEéÉ][\s]?[rR][\s]?[iI][\s]?[eE][\s]?[nN][\s]?[cC][\s]?[eE]|E[mM][pP][lL][oO][yY][Mm][eE][nN][tT]')
            matches = re.findall(pattern, sentence)
            if(len(matches)!=0):
                expBloc=True
                eduBloc=False
                certBloc=False
            pattern1 = re.compile(r'P[aA][rR][cC][oO][uU][rR][sS]?|D[iI][pP][lL][oO][mM][aA][sS]|[dD][eE][gG][rR][eE][eE]|F[\s]?[oO][\s]?[rR][\s]?[mM][\s]?[aA][\s]?[tT][\s]?[iI][\s]?[Oo][\s]?[Nn]|[EÉ][\s]?[dD][\s]?[uU][\s]?[cC][\s]?[aA][\s]?[tT][\s]?[iI][\s]?[oO][\s]?[nN]|[P][aA][rR][cC][oO][uU][rR][sS]?[\s]*[A][Cc][aA][dD][eE][mM][iI][qQ][uU][eE]|[D][iI][pP][lL][oOôÔ][Mm][eE][sS]|E[tT][uU][dD][eE][sS]|A[Cc][aA][dD][eE][mM][iI][Cc][sS]')
            matches1 = re.findall(pattern1, sentence)
            if(len(matches1)!=0):
                expBloc=False
                eduBloc=True
                certBloc=False


            

            if(expBloc==True)and(self.is_empty_or_spaces(sentence)!=True):
                listExperience.append(sentence)
            if(eduBloc==True)and(self.is_empty_or_spaces(sentence)!=True):
                listEducation.append(sentence)
        listEducation=listEducation[1:]
        listExperience=listExperience[1:]
        typleOfEperiencesAndEducation=(listEducation,listExperience)
        return typleOfEperiencesAndEducation
    
    def getListEduOrg(self,text):    
        listOfsentences=text.split("\n")
        #print(text)
        typlesOfExperienceAndEducation=self.getTypleOfExperienceAndEducation(listOfsentences)
        listEducation=typlesOfExperienceAndEducation[0]
        listExperience=typlesOfExperienceAndEducation[1]
        #print(listEducation)
        #print(listExperience)
        listEduDate=[] #registre all the date for the Education
        listEduOrg=[] #list of the educationnal organization
        for sentence in listEducation:
            if(len(self.isdate(sentence))):
                listEduDate.append(sentence)

            if(len(self.isDiplomat(sentence))!=0):
                listEduOrg.append(sentence)
        return listEduOrg