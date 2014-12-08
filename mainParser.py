import json
import jsonClasses

mapping = {
    'area': jsonClasses.Area,
    'labeled': jsonClasses.Labeled,
    'interval': jsonClasses.Interval,
    'sum_interval': jsonClasses.SumInterval,
    'difference_interval': jsonClasses.DifferenceInterval,
    }

jsonFile = open('config_new.json')
json = json.load(jsonFile)

for categoryName, category in json.items():
    for entry in category['entries']
        type = entry['type']
        jsonObject = mapping[type](entry)

jsonFile.close()
