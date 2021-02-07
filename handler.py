import os
import json
import boto3
import arrow
import getOdds
import getResults
from dtbInterface import DbInterface


def updateOdds(event, context):
    db = DbInterface()
    status, statusMsg, matches = getOdds.parseJson()
    db.updateOdds(matches)

    body = {"message": statusMsg, "matches": len(matches), "input": event}
    statusCode = 400
    if status:
        statusCode = 200

    response = {"statusCode": statusCode, "body": json.dumps(body)}

    return response


def updateResults(event, context):
    db = DbInterface()
    status, statusMsg, results = getResults.parseJson()
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
    waitInterval = 4
    waitTime = getWaitTime(waitInterval)

    print(os.environ["ODDS_ARN"])
    client = boto3.client("stepfunctions")
    inputStr = '{"waitUntil": "' + waitTime + '"}'
    response = client.start_execution(
        stateMachineArn=os.environ["ODDS_ARN"], input=inputStr
    )

    return {
        "message": "I just scheduled the next odds update",
        "executionArn": response["executionArn"],
    }


def ScheduleResults(event, context):
    waitInterval = 1
    waitTime = getWaitTime(waitInterval)

    client = boto3.client("stepfunctions")
    inputStr = '{"waitUntil": "' + waitTime + '"}'
    response = client.start_execution(
        stateMachineArn=os.environ["RESULTS_ARN"], input=inputStr
    )

    return {
        "message": "I just scheduled the next odds update",
        "executionArn": response["executionArn"],
    }


def getWaitTime(interval):
    now = arrow.utcnow()

    time = now.shift(hours=interval)

    ret = time.for_json()

    return ret
