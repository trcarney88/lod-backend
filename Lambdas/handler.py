import os
import json
import boto3
import Utils
import UpdateOdds
import UpdateResults
from dtbInterface import DbInterface
import StepFunctions
import ApiFunctions


def updateOdds(event, context):
    db = DbInterface()
    status, statusMsg, matches = UpdateOdds.parseJson()
    db.updateOdds(matches)

    body = {"message": statusMsg, "matches": len(matches), "input": event}
    statusCode = 400
    if status:
        statusCode = 200

    response = {"statusCode": statusCode, "body": json.dumps(body)}

    return response


def updateResults(event, context):
    db = DbInterface()
    status, statusMsg, results = UpdateResults.parseJson()
    updated = db.updateResults(results)

    body = {
        "message": statusMsg,
        "results": len(results),
        "input": event,
        "updated": updated,
    }
    statusCode = 400
    if status:
        statusCode = 200

    response = {"statusCode": statusCode, "body": json.dumps(body)}

    return response


def ScheduleOdds(event, context):
    return StepFunctions.ScheduleOdds()


def ScheduleResults(event, context):
    return StepFunctions.ScheduleResults()

def GetOdds(event, context):
    body = ApiFunctions.GetOdds()
    resp = {
        "statusCode": 200,
        "body": body,
        "isBase64Encoded": False
    }

    return resp