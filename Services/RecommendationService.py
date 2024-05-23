from Services.MySqlService import MySqlService
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class RecommendationService:
    def processConsultant(self,consultant):
        description=""
        experienceList=consultant.get('experienceList')
        educationList=consultant.get('educationList')
        listSkills=consultant.get('listSkills')
        if(educationList==None):
            educationList=[]
        if(experienceList==None):
            experienceList=[]
        if(listSkills==None):
            experienceList=[]
        for i in range(len(experienceList)):
            description+=experienceList[i].get('title')+' '
        for i in range(len(educationList)):
            description+=educationList[i].get('title')+' '
        for i in range(len(listSkills)):
            description+=listSkills[i].get('name')+' '
        return description
    def getOpportunityList(self,mysql):
        mysqlService=MySqlService()
        data= mysqlService.getAllOpportunity(mysql)
        
        # Convert the query result into a list of dictionaries
        table_dict_list = [{'id': item[0], 'titre': item[1], 'description': item[2],'date':item[3],'tjm':item[4],'duree':item[5],'location':item[6]} for item in data]
        
        # Convert the list of dictionaries into a DataFrame
        df = pd.DataFrame(table_dict_list)
        #print(df)
        return df
    
    def opportunityListToDataFrame(self,df1):
        columns_to_keep = ['titre', 'description', 'date','tjm','duree','location']  # Specify the columns you want to keep
        df1 = df1[columns_to_keep]
        return df1
    
    def addConsultant(self,consultantDescription,df1):
        df1.loc[len(df1)]=['Notre',consultantDescription,'','','','']
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
    
    def getRecommendationOpportunity(self,mysql,consultant):
        df1=self.getOpportunityList(mysql)
        df1=self.opportunityListToDataFrame(df1)
        
        df1['description']=df1['description'].fillna('')
        #df1['description']=df1['titre']+df1['description']
        df1['description']=df1['description']+df1['titre']
        consultantDescription=self.processConsultant(consultant)
        df1=self.addConsultant(consultantDescription,df1)
        # Append the new row to the DataFrame
        tdif_matrix=self.vectorization(df1)
        cosine_sim=linear_kernel(tdif_matrix,tdif_matrix)
        indices=pd.Series(df1.index, index=df1['titre']).drop_duplicates()
        df=self.get_recommendation('Notre',cosine_sim,indices,df1).copy()
        
        df = df.drop(index=len(df)-1)

        return self.dataframeToObjectList(df)