import requests
import json
import time
from src.db.redis import redis_instance

def wx_access_token():
    appId = "wx0241c6780dee0df3"
    appSecret = "ff3ef3a4812349d075db58aa568239b0"
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appId, appSecret)
    response = requests.get(url)
    response.encoding = "utf-8"
    jsonDict = json.loads(response.text)
    jsonDict['timestamp'] = time.time()
    redis_instance.hmset("wx_access_token", jsonDict)
    return jsonDict

def get_access_token_from_cache():
    token = redis_instance.hget("wx_access_token", "access_token")
    return bytes(token).decode()