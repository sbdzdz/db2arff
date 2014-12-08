import json
import jsonReader

mapping = {
    'area': jsonReader.Area,
    'labeled': jsonReader.Labeled,
    'interval': jsonReader.Interval,
    'sum_interval': jsonReader.SumInterval,
    'difference_interval': jsonReader.DifferenceInterval,
    }

jsonFile = open('config_new.json')
json = json.load(jsonFile)

for category in json:
    for entry in json[category]:
        for element in json[category][entry]:


jsonFile.close()
