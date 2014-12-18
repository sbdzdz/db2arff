from jsonParser import JSONParser

jsonFileName = 'config_new.json'
start = 0
end = 1390510940000
deviceID = '92d47d9d-a600-4309-b340-b58314c2e429'

parser = JSONParser(jsonFileName)
parser.generateArff(deviceID, start, end)
