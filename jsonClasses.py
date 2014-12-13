import pymysql as db
import numpy as np
import configparser as cp


class JSONType:

    configFileName = 'connection.conf'
    deviceID = '92d47d9d-a600-4309-b340-b58314c2e429' 

    def __init__(self, categoryName, jsonObject):
        self.categoryName = categoryName
        self.source = jsonObject['source']
        self.data = jsonObject['data']
    
    def getData(self, deviceID, start, end):
        query = self.generateQuery(deviceID, start, end)
        connection = self.establishConnection(self.configFileName)
        cursor = connection.cursor()
        cursor.execute(query)
        data = [row[1] for row in cursor]
        return data

    def classifyData(self, values):
        labels = self.getLabels()
        bins = self.getBins()
        values = self.getData()
        classifiedData = [labels[point] for point in np.digitize(values, np.array(bins))]
        return classifiedData

    def getLabels(self):
        labels = [interval['label'] for interval in self.data]
        return labels
    
    def getBins(self):
        leftEdges = [interval['from'] for interval in self.data]
        rightEdges = [interval['to'] for interval in self.data]
        union = set(leftEdges + right Edges)
        edges = sorted(list(union))
        bins = np.array(edges[1:-1]) #open outer ranges
        return bins

    def establishConnection(self, configFile):
        config = cp.ConfigParser()
        config.read(configFile)
        connection = db.connect(
            host = config['connection']['host'],
            user = config['connection']['user'],
            password = config['connection']['password'],
            db = config['connection']['name']
            )
        return connection
        
    def generateQuery(self, deviceID, start, end):
        query = (
            'select timestamp, {0} '
            'from {1} '
            'where device_id ="{2}" '
            'and timestamp>={3} '
            'and timestamp<={4}'
            ).format(self.source, self.categoryName, deviceID, start, end)
        return query
            
class Area(JSONType):
    
    def __init__(self, categoryName, jsonObject):
        self.categoryName = categoryName
        self.sourceX = jsonObject['source_x']
        self.sourceY = jsonObject['source_y']
        self.data = jsonObject['data']


class Labeled(JSONType):
    pass
    
class Interval(JSONType):
class SumInterval(JSONType):#Interval):
    def __init__(self, categoryName, jsonObject):
        self.categoryName = categoryName
        self.source = jsonObject['source']
        self.data = jsonObject['data']
        self.window = jsonObject['window']

class DifferenceInterval(JSONType):#Interval):
    def __init__(self, categoryName, jsonObject):
        self.categoryName = categoryName
        self.sourceBegin = jsonObject['source_begin']
        self.sourceEnd = jsonObject['source_end']
        self.data = jsonObject['data']


        
