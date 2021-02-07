import sys
import os
import json
import requests

endpoint = "https://api.jsonodds.com//api/odds"


class OddsDetails:
    oid = ""
    oddType = ""
    moneyLineAway = ""
    moneyLineHome = ""
    drawLine = ""
    overLine = ""
    totalNumber = ""
    underLine = ""
    pointSpreadAway = ""
    pointSpreadHome = ""
    pointSpreadAwayLine = ""
    pointSpreadHomeLine = ""
    lastUpdated = ""

    def __init__(self):
        self.oid = ""
        self.oddType = ""
        self.moneyLineAway = ""
        self.moneyLineHome = ""
        self.drawLine = ""
        self.overLine = ""
        self.totalNumber = ""
        self.underLine = ""
        self.pointSpreadAway = ""
        self.pointSpreadHome = ""
        self.pointSpreadAwayLine = ""
        self.pointSpreadHomeLine = ""
        self.lastUpdated = ""

    def jsonDatatoOddsDetails(self, jsonData):
        for key in jsonData.keys():
            if key == "LastUpdated":
                self.lastUpdated = str(jsonData[key])
            elif key == "PointSpreadAwayLine":
                self.pointSpreadAwayLine = str(jsonData[key])
            elif key == "PointSpreadHomeLine":
                self.pointSpreadHomeLine = str(jsonData[key])
            elif key == "MoneyLineHome":
                self.moneyLineHome = str(jsonData[key])
            elif key == "OverLine":
                self.overLine = str(jsonData[key])
            elif key == "MoneyLineAway":
                self.moneyLineAway = str(jsonData[key])
            elif key == "TotalNumber":
                self.totalNumber = str(jsonData[key])
            elif key == "UnderLine":
                self.underLine = str(jsonData[key])
            elif key == "PointSpreadHome":
                self.pointSpreadHome = str(jsonData[key])
            elif key == "PointSpreadAway":
                self.pointSpreadAway = str(jsonData[key])
            elif key == "OddType":
                self.oddType = str(jsonData[key])
            elif key == "DrawLine":
                self.drawLine = str(jsonData[key])
            elif key == "ID":
                self.oid = jsonData[key].replace("-", "")
            else:
                continue


class MatchDetails:
    eventId = ""
    homeTeam = ""
    awayTeam = ""
    sport = ""
    matchTime = ""
    league = ""
    details = ""
    homePitcher = ""
    awayPitcher = ""
    oddsList = []

    def __init__(self):
        self.eventId = ""
        self.homeTeam = ""
        self.awayTeam = ""
        self.sport = ""
        self.matchTime = ""
        self.league = ""
        self.details = ""
        self.homePitcher = ""
        self.awayPitcher = ""
        self.oddsList = []

    def jsonDatatoMatchDetails(self, match):
        for key in match.keys():
            if key == "HomeTeam":
                self.homeTeam = str(match[key])
            elif key == "AwayPitcher":
                self.awayPitcher = str(match[key])
            elif key == "HomePitcher":
                self.homePitcher = str(match[key])
            elif key == "Sport":
                self.sport = str(match[key])
            elif key == "MatchTime":
                self.matchTime = str(match[key])
            elif key == "League":
                self.league = str(match[key]['Name'])
            elif key == "Details":
                self.details = str(match[key])
            elif key == "AwayTeam":
                self.awayTeam = str(match[key])
            elif key == "ID":
                self.eventId = match[key].replace("-", "")
            elif key == "Odds":
                for oddObj in match[key]:
                    oddDetail = OddsDetails()
                    oddDetail.jsonDatatoOddsDetails(jsonData=oddObj)
                    self.oddsList.append(oddDetail)
            else:
                continue


def parseJson():
    status = True
    statusMsg = "All Good!"
    jsonData = []
    api_key = os.environ["API_KEY"]

    matches = []

    try:
        r = requests.get(endpoint, headers={"x-api-key": api_key})

        if r.status_code == requests.codes['ok']:
            jsonData = r.json()

            for match in jsonData:
                matchDetails = MatchDetails()
                matchDetails.jsonDatatoMatchDetails(match=match)
                matches.append(matchDetails)

            return [status, statusMsg, matches]
        else:
            status = False
            statusMsg = "JsonOdds API Error: " + r.text
            return [status, statusMsg, []]

    except:
        status = False
        statusMsg = (
            "Unexpected Exception was Thrown: "
            + str(sys.exc_info()[0])
            + " "
            + str(sys.exc_info()[1])
            + "; The error occured on line "
            + str(sys.exc_info()[2].tb_lineno)
        )
        return [status, statusMsg, []]


if __name__ == "__main__":
    status, statusMsg, matches = parseJson()

    print("Status: " + statusMsg)
    print("Number of Matches:", len(matches))
