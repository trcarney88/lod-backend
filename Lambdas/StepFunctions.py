import os
import boto3
import Utils

def ScheduleOdds():
    waitInterval = 4
    waitTime = Utils.getWaitTime(waitInterval)

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


def ScheduleResults():
    waitInterval = 1
    waitTime = Utils.getWaitTime(waitInterval)

    client = boto3.client("stepfunctions")
    inputStr = '{"waitUntil": "' + waitTime + '"}'
    response = client.start_execution(
        stateMachineArn=os.environ["RESULTS_ARN"], input=inputStr
    )

    return {
        "message": "I just scheduled the next results update",
        "executionArn": response["executionArn"],
    }