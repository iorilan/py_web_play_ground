import time
import json 
from bson import json_util, ObjectId

def now():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def mongoJson(mongoObjs):
    return json.loads(json_util.dumps(mongoObjs))
