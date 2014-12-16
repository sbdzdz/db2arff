import json
import jsonClasses

appropriateConstructor = {
    'area': jsonClasses.Area,
    'labeled': jsonClasses.Labeled,
    'interval': jsonClasses.Interval,
    'sum_interval': jsonClasses.SumInterval,
    'difference_interval': jsonClasses.TimeInterval,
    }

jsonFile = open('config_new.json')
json = json.load(jsonFile)

start = 0
end = 1390588135918
deviceID = '92d47d9d-a600-4309-b340-b58314c2e429' 

for categoryName, category in json.items():
    if categoryName == "time":
        continue
    for entry in category['entries']:
        type = entry['type']
        if type == 'sum_interval':
            continue
        jsonObject = appropriateConstructor[type](entry)
        data = jsonObject.getLabeledData(deviceID, start, end)
        print(data)
jsonFile.close()
