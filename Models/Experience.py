class Experience:
    def __init__(self, title,organisation):
        self.title = title
        self.company=organisation
        
    # Getter and Setter for title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value


    # Getter and Setter for start
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

