import json
import classes
import pandas as pd
import arff


class JSONParser:
    appropriateConstructor = {
        'area': classes.Area,
        'time': classes.Time,
        'labeled': classes.Labeled,
        'interval': classes.Interval,
        'sum_interval': classes.SumInterval,
        'difference_interval': classes.TimeInterval,
    }

    def __init__(self, jsonFileName):
        jsonFile = open(jsonFileName)
        self.json = json.load(jsonFile)
        jsonFile.close()

    def generateArff(self, deviceID, start, end):
        dataFrame = self.generateDataFrame(deviceID, start, end)
        headers = list(dataFrame.columns.values)
        out = open('out.arff', 'w')
        out.write("@RELATION aware\n\n")
        for header in headers:
            labels = ",".join(pd.unique(dataFrame[header].values)).replace(' ', '_')
            out.write("@ATTRIBUTE " + header + " {" + labels + "} %string\n")
        out.write("\n@DATA\n")
        for row in dataFrame.values:
            out.write(",".join(row).replace(' ', '_'))
            out.write("\n")
        out.close()
                   
    def generateDataFrame(self, deviceID, start, end):
        dataFrames = []
        for categoryName, category in self.json.items():
            for entry in category['entries']:
                type = entry['type']
                if type == 'time':
                    time = self.appropriateConstructor[type](entry)
                    continue
                else:
                    jsonObject = self.appropriateConstructor[type](entry)
                    data = jsonObject.getLabeledData(deviceID, start, end)
                    dataFrames.append(data)
        result = pd.concat(dataFrames, axis = 1).ffill().bfill()
        result.index = pd.to_datetime(result.index, unit = 'ms')
        timeLabeled = time.labelData(result.index.hour)
        result['time'] = pd.Series(timeLabeled, result.index)
        return result
