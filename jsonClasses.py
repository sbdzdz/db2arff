class JSONType:
    def __init__(self, jsonObject):
        self.source = jsonObject['source']
        self.data = jsonObject['data']

class Area(JSONType):
    def __init__(self, jsonObject):
        self.sourceX = jsonObject['source_x']
        self.sourceY = jsonObject['source_y']
        self.data = jsonObject['data']

class Labeled(JSONType):
    pass

class Interval(JSONType):
    pass

class SumInterval(Interval):
    def __init__(self, jsonObject):
        self.source = jsonObject['source']
        self.data = jsonObject['data']
        self.window = jsonObject['window']

class DifferenceInterval(Interval):
    def __init__(self, jsonObject):
        self.sourceBegin = jsonObject['source_begin']
        self.sourceEnd = jsonObject['source_end']
        self.data = jsonObject['data']


        
