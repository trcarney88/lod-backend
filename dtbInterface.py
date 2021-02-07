import os
import boto3
from boto3.dynamodb.conditions import Key
import arrow

class DbInterface:
    client = None
    oddsTable = None
    oddsSet = None
    resultsSet = None

    def __init__(self):
        self.client = boto3.client('dynamodb')
        self.oddsTable = os.environ['CF_OddsTable']
        self.oddsSet = set()
        self.resultsSet = set()

    def updateOdds(self, matches):
        for match in matches:
            for odds in match.oddsList:
                if odds.oid not in self.oddsSet and odds.oddType == 'Game':
                    self.oddsSet.add(odds.oid)
                    idCheck = self.client.query(
                        TableName=self.oddsTable,
                        KeyConditionExpression='id = :oid',
                        ExpressionAttributeValues={
                            ':oid': {'S': odds.oid}
                        }
                    )

                    if len(idCheck['Items']) > 0:
                        resp = self.client.update_item(
                            TableName=self.oddsTable,
                            Key={
                                'id': {'S': odds.oid}
                            },
                            AttributeUpdates={
                                'MatchTime':{
                                    'Action': 'PUT',
                                    'Value': {'S': match.matchTime}
                                },
                                'Details': {
                                    'Action': 'PUT',
                                    'Value': {'S': match.details}
                                },
                                'HomePitcher': {
                                    'Action': 'PUT',
                                    'Value': {'S': match.homePitcher}
                                },
                                'AwayPitcher': {
                                    'Action': 'PUT',
                                    'Value': {'S': match.awayPitcher}
                                },
                                'MoneyLineAway': {
                                    'Action': 'PUT',
                                    'Value': {'S': odds.moneyLineAway}
                                },
                                'MoneyLineHome': {
                                    'Action': 'PUT',
                                    'Value': {'S': odds.moneyLineHome}
                                },
                                'DrawLine': {
                                    'Action': 'PUT',
                                    'Value': {'S': odds.drawLine}
                                },
                                'OverLine': {
                                    'Action': 'PUT',
                                    'Value': {'S': odds.overLine}
                                },
                                'UnderLine': {
                                    'Action': 'PUT',
                                    'Value': {'S': odds.underLine}
                                },
                                'TotalNumber': {
                                    'Action': 'PUT',
                                    'Value': {'S': odds.totalNumber}
                                },
                                'PointsSpreadAway': {
                                    'Action': 'PUT',
                                    'Value': {'S': odds.pointSpreadAway}
                                },
                                'PointsSpreadHome': {
                                    'Action': 'PUT',
                                    'Value': {'S': odds.pointSpreadHome}
                                },
                                'PointsSpreadAwayLine': {
                                    'Action': 'PUT',
                                    'Value': {'S': odds.pointSpreadAwayLine}
                                },
                                'PointsSpreadHomeLine': {
                                    'Action': 'PUT',
                                    'Value': {'S': odds.pointSpreadHomeLine}
                                },
                                'LastUpdated': {
                                    'Action': 'PUT',
                                    'Value': {'S': odds.lastUpdated}
                                }
                            }
                        )
                    else:
                        resp = self.client.put_item(
                            TableName=self.oddsTable,
                            Item={
                                'id': {'S': odds.oid},
                                'HomeTeam': {'S': match.homeTeam},
                                'AwayTeam': {'S': match.awayTeam},
                                'Sport': {'S': match.sport},
                                'MatchTime':{'S': match.matchTime},
                                'League': {'S': match.league},
                                'Details': {'S': match.details},
                                'HomePitcher': {'S': match.homePitcher},
                                'AwayPitcher': {'S': match.awayPitcher},
                                'MoneyLineAway': {'S': odds.moneyLineAway},
                                'MoneyLineHome': {'S': odds.moneyLineHome},
                                'DrawLine': {'S': odds.drawLine},
                                'OverLine': {'S': odds.overLine},
                                'UnderLine': {'S': odds.underLine},
                                'TotalNumber': {'S': odds.totalNumber},
                                'PointsSpreadAway': {'S': odds.pointSpreadAway},
                                'PointsSpreadHome': {'S': odds.pointSpreadHome},
                                'PointsSpreadAwayLine': {'S': odds.pointSpreadAwayLine},
                                'PointsSpreadHomeLine': {'S': odds.pointSpreadHomeLine},
                                'LastUpdated': {'S': odds.lastUpdated}
                            }
                        )

    def updateResults(self, results):
        updated = 0
        for result in results:
            if result.id not in self.resultsSet and result.oddType == 'Game':
                self.resultsSet.add(result.id)
                idCheck = self.client.query(
                        TableName=self.oddsTable,
                        KeyConditionExpression='id = :oid',
                        ExpressionAttributeValues=
                        {
                            ':oid': {'S': result.id}
                        }
                    )
                if len(idCheck['Items']) > 0:
                    updated += 1
                    resp = self.client.update_item(
                            TableName=self.oddsTable,
                            Key={
                                'id': {'S': result.id}
                            },
                            AttributeUpdates={
                                'HomeScore':{
                                    'Action': 'PUT',
                                    'Value': {'S': result.homeScore}
                                },
                                'AwayScore': {
                                    'Action': 'PUT',
                                    'Value': {'S': result.awayScore}
                                },
                                'Final': {
                                    'Action': 'PUT',
                                    'Value': {'S': result.final}
                                },
                                'BinaryScore': {
                                    'Action': 'PUT',
                                    'Value': {'S': result.binaryScore}
                                },
                                'FinalPosition': {
                                    'Action': 'PUT',
                                    'Value': {'S': result.finalPosition}
                                },
                                'AETScore': {
                                    'Action': 'PUT',
                                    'Value': {'S': result.aetScore}
                                },
                                'PKScore': {
                                    'Action': 'PUT',
                                    'Value': {'S': result.pkScore}
                                }
                            }
                        )
                    return updated
