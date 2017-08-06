import pymysql as db
import numpy as np
import configparser as cp
from shapely.geometry import Point, Polygon
import pandas as pd

class JSONType:

    configFileName = 'connection.conf'

    def __init__(self, jsonObject):
        self.table = jsonObject['table']
        self.column = jsonObject['column']
        self.name = jsonObject['name']
        self.intervals = jsonObject['intervals']

    def getLabeledData(self, deviceID, start, end):
        data = self.getData(deviceID, start, end)
        timestamps = [row[0] for row in data]
        values = [row[1] for row in data]
        labeledValues = self.labelData(values)
        labeledData = pd.DataFrame(data = labeledValues, index = timestamps, columns = ["{0}:{1}".format(self.table, self.name)])
        return labeledData
    
    def getData(self, deviceID, start, end):
        query = self.generateQuery(deviceID, start, end)
        connection = self.establishConnection(self.configFileName)
        data = self.executeQuery(query, connection)
        return(data)

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
            ).format(self.column, self.table, deviceID, start, end)
        return query

    def executeQuery(self, query, connection):
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def labelData(self, data):
        labels = self.getLabels()
        classifiedData = self.classifyData(data)
        labeledData = [labels[point] for point in classifiedData]
        return labeledData

    def getLabels(self):
        labels = [interval['label'] for interval in self.intervals]
        return labels
    
    def classifyData(self, data):
        bins = self.getBins()
        classifiedData = np.digitize(data, bins)
        return classifiedData

    def getBins(self):
        leftEdges = [interval['from'] for interval in self.intervals]
        rightEdges = [interval['to'] for interval in self.intervals]
        union = set(leftEdges + rightEdges)
        edges = sorted(list(union))
        bins = np.array(edges[1:-1]) #open outer ranges
        return bins

class Time(JSONType):
    def __init__(self, jsonObject):
        self.name = jsonObject['name']
        self.intervals = jsonObject['intervals']

class Area(JSONType):
    def __init__(self, jsonObject):
        self.table = jsonObject['table']
        self.columnX = jsonObject['column_x']
        self.columnY = jsonObject['column_y']
        self.name = jsonObject['name']
        self.intervals = jsonObject['intervals']
        
    def generateQuery(self, deviceID, start, end):
        query = (
            'select timestamp, {0}, {1} '
            'from {2} '
            'where device_id ="{3}" '
            'and timestamp>={4} '
            'and timestamp<={5}'
            ).format(self.columnX, self.columnY, self.table, deviceID, start, end)
        return query
        
    def executeQuery(self, query, connection):
        cursor = connection.cursor()
        cursor.execute(query)
        data = [(row[0], Point(row[1], row[2])) for row in cursor]
        return data

    def labelData(self, data):
        labels = self.getLabels()
        labeledData = [self.classifyPoint(point, labels) for point in data]
        return labeledData
    
    def classifyPoint(self, point, labels):
        match = next((labels[polygon] for polygon in labels if polygon.contains(point)), "Other")
        return match

    def getLabels(self):
        labels = {self.createPolygon(interval['vertices']) : interval['label'] for interval in self.intervals}
        return labels
    
    def createPolygon(self, vertices):
        vertexList = [(vertex['latitude'], vertex['longitude']) for vertex in vertices]
        polygon = Polygon(vertexList)
        return polygon

class Labeled(JSONType):

    def labelData(self, data):
        labels = self.getLabels()
        labeledData = [labels.get(point, point) for point in data]
        return labeledData

    def getLabels(self):
        labels = {key: interval['label'] for interval in self.intervals for key in interval['included']}
        return labels
    
class Interval(JSONType):
    pass

class SumInterval(Interval):
    pass

class TimeInterval(Interval):
    pass
    def generateQuery(self, deviceID, start, end):
        query = (
            'select timestamp, `{0}`-`timestamp` as `usage` '
            'from {1} '
            'where device_id ="{2}" '
            'and timestamp>={3} '
            'and timestamp<={4}'
            ).format(self.column, self.table, deviceID, start, end)
        return query
    


        
