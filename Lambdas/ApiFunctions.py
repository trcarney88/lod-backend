import os
import arrow
import json
from dtbInterface import DbInterface

def GetOdds(**kwargs):
    db = DbInterface()
    items = db.GetAllOdds()
    ret = []

    now = arrow.utcnow()

    for item in items:
        matchTime = arrow.get(item['MatchTime']['S'])
        if matchTime < now:
            for key in item.keys():
                item[key] = item[key]['S']
            
            ret.append(item)

    return json.dumps(ret)