class Consultant:
    def __init__(self, name, email,linkedIn,phoneNumber,languages, listSkills=None,educationList=None,experienceList=None):
        self.name = name
        self.email = email
        self.linkedIn=linkedIn
        self.phoneNumber=phoneNumber
        self._languages = languages if languages else []
        self.listSkills = listSkills if listSkills else []
        self.educationList=educationList
        self.experienceList=experienceList

    def add_skill(self, skill):
        self.listSkills.append(skill)
    
    def setName(self,name):
        self.name=name
    
    @property
    def languages(self):
        return self._languages

    @languages.setter
    def languages(self, new_languages):
        self._languages = new_languages
    
    def add_language(self, language):
        self._languages.append(language)

    def remove_language(self, language):
        if language in self._languages:
            self._languages.remove(language)
        else:
            print(f"{self._name} does not have the language {language}.")
    
    def getName(self):
        return self.name
    

    def setEmail(self,email):
        self.email=email

    def getEmail(self):
        return self.email
    
    def setLinkedIn(self,linkedIN):
        self.linkedIn=linkedIN

    def getLinkIn(self):
        return self.getLinkIn
    
    def setPhoneNumber(self,phoneNumber):
        self.phoneNumber=phoneNumber

    def getPhoneNumber(self):
        return self.phoneNumber
    
    def getEducationList(self):
        return self.educationList
    
    def setEducationList(self,educationList):
        self.educationList=educationList
        
    def getListSkill(self):
        return self.listSkills
    
    def setListSkills(self,listSkills):
        self.listSkills=listSkills

    def remove_skill(self, skill):
        if skill in self.listSkills:
            self.listSkills.remove(skill)
        else:
            print(f"{self.name} does not have the skill {skill}.")

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print("Skills:", ', '.join(self.listSkills))