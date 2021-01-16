import sys
import os
import json
import requests

endpoint = "https://api.jsonodds.com//api/results"

finalTypes = [
    "NotFinished",
    "Finished",
    "Postponed",
    "Canceled",
    "Abandoned",
    "Retired",
    "TeamOneWithdrew",
    "TeamTwoWithdrew",
    "Scratched"
]

class Result:
    id = None
    homeScore = None
    awayScore = None
    final = None
    eventId = None
    oddType = None
    finalType = None
    binaryScore = None
    name = None
    finalPosition = None
    aetScore = None
    pkScore = None

    def __init__(self):
        self.id = ""
        self.homeScore = "0"
        self.awayScore = "0"
        self.final = ""
        self.eventId = ""
        self.oddType = ""
        self.finalType = ""
        self.binaryScore = "0-0"
        self.name = ""
        self.finalPosition = "0"
        self.aetScore = "0-0"
        self.pkScore = "0-0"

    def jsonToResult(self, jsonData):
        for key in jsonData.keys():
            if key == 'EventID':
                self.eventId = jsonData[key].replace('-', '')
            elif key == 'BinaryScore':
                self.binaryScore = str(jsonData[key])
            elif key == 'HomeScore':
                self.homeScore = str(jsonData[key])
            elif key == 'AwayScore':
                self.awayScore = str(jsonData[key])
            elif key == 'OddType':
                self.oddType = str(jsonData[key])
            elif key == 'ID':
                self.id = jsonData[key].replace('-', '')
            elif key == 'FinalType':
                self.finalType = str(jsonData[key])
            elif key == 'Name':
                self.name = str(jsonData[key])
            elif key == 'FinalPosition':
                self.finalPosition = str(jsonData[key])
            elif key == 'Final':
                self.final = str(jsonData[key])
            elif key == 'AETScore':
                self.aetScore = str(jsonData[key])
            elif key == 'PKScore':
                self.pkScore = str(jsonData[key])
            else:
                continue
    
def parseJson():
    status = True
    statusMsg = "All Good!"
    jsonData = []
    api_key = os.environ['API_KEY']
    
    results = []

    try:
        r = requests.get(endpoint, headers={'x-api-key': api_key})

        if r.status_code == requests.codes.ok:
            jsonData = r.json()
                       
            for data in jsonData:
                r = Result()
                r.jsonToResult(data)
                results.append(r)
            
            return [status, statusMsg, results]
        else:
            status = False
            statusMsg = "JsonOdds API Error: " + r.text
            return [status, statusMsg, []]

    except:
        status = False
        statusMsg = "Unexpected Exception was Thrown: " + str(sys.exc_info()[0]) + ' ' + str(sys.exc_info()[1]) + '; The error occured on line ' + str(sys.exc_info()[2].tb_lineno)
        return [status,statusMsg, []]

if __name__ == '__main__':
    status, statusMsg, results = parseJson()
    print(statusMsg)
    print('Results:', len(results))