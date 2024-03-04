class Education:
    def __init__(self, title,organisation,start,end):
        self.title = title
        self.organisation=organisation
        self.start=start
        self.end=end
        
    # Getter and Setter for title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    # Getter and Setter for organisation
    @property
    def organisation(self):
        return self._organisation

    @organisation.setter
    def organisation(self, value):
        self._organisation = value

    # Getter and Setter for start
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    # Getter and Setter for end
    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value