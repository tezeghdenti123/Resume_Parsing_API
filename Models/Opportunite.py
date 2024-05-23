class Opportunite:
    def __init__(self, titre,description,dateDeposition,tjm,durée,location):
        self.titre = titre
        self.description=description
        self.date=dateDeposition
        self.tjm=tjm
        self.duree=durée
        self.location=location
    @property
    def titre(self):
        return self._titre

    @titre.setter
    def titre(self, value):
        self._titre = value
    
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
    
    
    @property
    def tjm(self):
        return self._tjm

    @tjm.setter
    def tjm(self, value):
        self._tjm = value

  
    
    @property
    def location(self):
        return self._durée

    @location.setter
    def location(self, value):
        self._location = value



    