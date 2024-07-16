from openai import OpenAI
import streamlit as st
import instructor
from pydantic import BaseModel
from typing import List
import nltk
from nltk.tokenize import sent_tokenize

# Download the necessary resources
nltk.download('punkt')
class Experience(BaseModel):
    title: str
    company: str

class ResponseModel(BaseModel):
    listOfExperience: List[Experience]
class ExperienceExtractService:
    def extractExperience(self,prompt):
        #create the client
        client =OpenAI(
            api_key='jjjjjdffhfhfhf',
            base_url='http://localhost:8000/v1'
        )
        client=instructor.patch(client=client)
        
        prompt1="Please extract all experiences mentioned in the provided text. An experience typically consists of a title and a company name. Ensure that the extracted experiences are in the following format: \n Experience \n - Title: [Title 1] \n - Company: [Company 1] \n Experience 2: \n - Title: [Title 2] \n - Company: [Company 2] \n And so on... \n Text:"
        prompt=prompt1+prompt
        #chat completion
        response=client.chat.completions.create(
            #which model we want to use
            model='/Hermes-2-Pro-Mistral-7B.Q4_K_M.gguf',
            #pass through our prompt
            messages=[{
                'role':'user',
                'content':prompt
            }],
            response_model=ResponseModel,
            

        )
        print(response)

    def getListExperience(self,text):
        listexperience=[]
        sentences = sent_tokenize(text)

        # Iterate over each sentence
        '''for sentence in sentences:
            print(sentence)'''
        listExperience=self.extractExperience(sentences[11])
        return listexperience