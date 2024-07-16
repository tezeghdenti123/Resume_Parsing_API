from Services.MySqlService import MySqlService
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from Services.CandidateDBService import CandidateDBService
from Services.ResumeParserService import Service

class CandidateRecommendationService:
    def processConsultant(self,consultant):
        description=consultant.getTitle()+' '
        experienceList=consultant.getExperienceList()
        educationList=consultant.getEducationList()
        listSkills=consultant.getListSkill()
        
        if(educationList==None):
            educationList=[]
        if(experienceList==None):
            experienceList=[]
        if(listSkills==None):
            experienceList=[]
        for i in range(len(experienceList)):
            description+=experienceList[i].title()+' '
        for i in range(len(listSkills)):
            description+=listSkills[i].get('name')+' '
        for i in range(len(educationList)):
            description+=educationList[i].get('_title')+' '
        
        return description
    def getCandidateList(self,offreId):
        ##mysqlService=MySqlService()
        ##data= mysqlService.getAllOpportunity(mysql)
        candidateDBService=CandidateDBService()
        data=candidateDBService.get_candidate_profile(offreId)
        # Convert the query result into a list of dictionaries
        
        #print(df)
        return data
    
    def candidateListToDataFrame(self,data,tagger):
        resumeParserService=Service()
        candidateDataFrame=[]
        for candidate in data:
            candidate['_id'] = str(candidate['_id'])  # Convert ObjectId to string
            cv_file = candidate['cv_file']
            text=Service.extract_content(cv_file)
            candidateProfile=Service.ResumeToConsultant(text,tagger)
            candidateProfile.setName(candidate['name'])
            candidateProfile.setTitle(candidate['title'])
            candidateProfile.setEmail(candidate['email'])
            candidateProfile.setPhoneNumber(candidate['phone'])
            description=self.processConsultant(candidateProfile)
            candidateDataFrame.append({'id':candidate['_id'],'name':candidateProfile.getName(),'title':candidateProfile.getTitle(),'email':candidateProfile.getEmail(),'phone':candidateProfile.getPhoneNumber(),'description':description})
        #table_dict_list = [{'id': item[0], 'titre': item[1], 'description': item[2],'date':item[3],'tjm':item[4],'duree':item[5],'location':item[6]} for item in data]
        
        # Convert the list of dictionaries into a DataFrame
        #df = pd.DataFrame(table_dict_list)
        #columns_to_keep = ['titre', 'description', 'date','tjm','duree','location']  # Specify the columns you want to keep
        #df1 = df1[columns_to_keep]
        df = pd.DataFrame(candidateDataFrame)
        return df
    
    def addOffre(self,offreDescription,df1):
        df1.loc[len(df1)]=['','','Notre','','',offreDescription]
        return df1
    
    def vectorization(self,df1):
        tdif=TfidfVectorizer(stop_words='english')
        tdif_matrix=tdif.fit_transform(df1['description'])
        return tdif_matrix
    
    def get_recommendation(self,title,cosine_sim,indices,df1):
        idx=indices[title]
        sim_scores=list(enumerate(cosine_sim[idx]))
        sim_scores=sorted(sim_scores,key=lambda X: X[1], reverse=True)
        #sim_scores=sim_scores[1:17]
        tech_indices=[i[0] for i in sim_scores]
        return df1.iloc[tech_indices]
    
    def dataframeToObjectList(self,df):
        row_objects = []
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            row_objects.append(row_dict)
        return row_objects
    def processOffre(self,offre):
        description=offre.get('title')+' '
        for item in offre.get('skills'):
            description+=item+' '
        description+=offre.get('description')+' '
        
        for item in offre.get('requirement'):
            description+=item+' '
        return description

    def getRecommendationOpportunity(self,offre,tagger):
        candidateList=self.getCandidateList(offre.get('id'))
        df1=self.candidateListToDataFrame(candidateList,tagger)
        
        #df1['description']=df1['titre']+df1['description']
        offreDescription=self.processOffre(offre)
        df1=self.addOffre(offreDescription,df1)
        # Append the new row to the DataFrame
        tdif_matrix=self.vectorization(df1)
        cosine_sim=linear_kernel(tdif_matrix,tdif_matrix)
        indices=pd.Series(df1.index, index=df1['title']).drop_duplicates()
        df=self.get_recommendation('Notre',cosine_sim,indices,df1).copy()
        
        df = df.drop(index=len(df)-1)

        return self.dataframeToObjectList(df)