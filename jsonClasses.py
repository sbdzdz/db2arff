class JSONType:
    def __init__(self, jsonObject):
        self.source = jsonObject['source']
        self.data = jsonObject['data']

class Area:(JSONType):
    def __init__(self, jsonObject):
        self.sourceX = jsonObject['source_x']
        self.sourceY = jsonObject['source_y']
        self.data = jsonObject['data']

class Labeled(JSONType):

class Interval(JSONType):

class SumInterval(Interval):
    def __init__(self, jsonObject):
        self.source = jsonObject['source']
        self.data = jsonObject['data']
        self.window = jsonObject['window']

class DifferenceInterval(Interval):
    def __init__(self, jsonObject):
        self.sourceBegin = jsonObject
        self.sourceEnd = sourceEnd
        self.data = data


        
