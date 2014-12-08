import numpy as np

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
    
class Interval(JSONType):
    def classify(self, values):
        labels = [interval['label'] for interval in data]
        bins = [interval['to'] for interval in data]
        return [labels[point] for point in np.digitize(values, np.array(bins)] 

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


        
