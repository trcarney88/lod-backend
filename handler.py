import json
import getOdds
import getResults


def updateOdds(event, context):
    status, statusMsg, matches = getOdds.parseJson()

    body = {
        "message": statusMsg,
        "matches": len(matches),
        "input": event
    }
    statusCode = 400
    if status:
        statusCode = 200
    
    response = {
        "statusCode": statusCode,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def updateResults(event, context):
    status, statusMsg, results = getResults.parseJson()

    body = {
        "message": statusMsg,
        "results": len(results),
        "input": event
    }
    statusCode = 400
    if status:
        statusCode = 200
    
    response = {
        "statusCode": statusCode,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

if __name__ == '__main__':
    print('Testing updateOdds...')
    resp = updateOdds('', '')
    print(resp)

    print('Testing updateResults...')
    resp = updateResults('', '')
    print(resp)