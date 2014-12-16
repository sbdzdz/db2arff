import pymysql as db
import numpy as np
import configparser as cp
from shapely.geometry import Point, Polygon

class JSONType:

    configFileName = 'connection.conf'

    def __init__(self, jsonObject):
        self.table = jsonObject['table']
        self.column = jsonObject['column']
        self.intervals = jsonObject['intervals']

    def getLabeledData(self, deviceID, start, end):
        data = self.getData(deviceID, start, end)
        labeledData = self.labelData(data)
        return labeledData
    
    def getData(self, deviceID, start, end):
        query = self.generateQuery(deviceID, start, end)
        connection = self.establishConnection(self.configFileName)
        data = self.executeQuery(query, connection)
        return data

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
            'select {0} '
            'from {1} '
            'where device_id ="{2}" '
            'and timestamp>={3} '
            'and timestamp<={4}'
            ).format(self.column, self.table, deviceID, start, end)
        return query

    def executeQuery(self, query, connection):
        cursor = connection.cursor()
        cursor.execute(query)
        data = [row[0] for row in cursor]
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
            
class Area(JSONType):
    def __init__(self, jsonObject):
        self.table = jsonObject['table']
        self.columnX = jsonObject['column_x']
        self.columnY = jsonObject['column_y']
        self.intervals = jsonObject['intervals']
        
    def generateQuery(self, deviceID, start, end):
        query = (
            'select {0}, {1} '
            'from {2} '
            'where device_id ="{3}" '
            'and timestamp>={4} '
            'and timestamp<={5}'
            ).format(self.columnX, self.columnY, self.table, deviceID, start, end)
        return query
        
    def executeQuery(self, query, connection):
        cursor = connection.cursor()
        cursor.execute(query)
        data = [Point(row[0], row[1]) for row in cursor]
        return data

    def labelData(self, data):
        labels = self.getLabels()
        classifiedData = self.classifyData(data)
        labeledData = [labels.get(point, "Other") for point in classifiedData]
        print(labeledData)
        return labeledData

    def classifyData(self, data):
        polygons = self.getPolygons()
        classifiedData = [polygon if polygon.contains(point) else None for polygon in polygons for point in data]
        return classifiedData

    def getPolygons(self):
        polygons = [self.createPolygon(interval['vertices']) for interval in self.intervals]
        return polygons
        
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
    def generateQuery(self, deviceID, start, end):
        query = (
            'select *, `{0}`-`timestamp` as `usage` '
            'from {1} '
            'where device_id ="{2}" '
            'and timestamp>={3} '
            'and timestamp<={4}'
            ).format(self.column, self.table, deviceID, start, end)
        return query

    


        
