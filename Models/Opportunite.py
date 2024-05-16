class Opportunite:
    def __init__(self, titre,description,dateDeposition,tjm,durée,location):
        self.titre = titre
        self.description=description
        self.dateDeposition=dateDeposition
        self.tjm=tjm
        self.durée=durée
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
    def dateDeposition(self):
        return self._deposition

    @dateDeposition.setter
    def dateDeposition(self, value):
        self._dateDeposition = value
    
    @property
    def tjm(self):
        return self._tjm

    @tjm.setter
    def tjm(self, value):
        self._tjm = value

    @property
    def durée(self):
        return self._durée

    @durée.setter
    def durée(self, value):
        self._durée = value
    
    @property
    def location(self):
        return self._durée

    @location.setter
    def location(self, value):
        self._location = value



    