from celery import shared_task
from src.service.wx_access_token import wx_access_token
from src.service.wx_media import get_complete_voice_reco

@shared_task()
def fresh_wx_access_token():
    res = wx_access_token()
    expire = res["expires_in"]
    print(res)
    fresh_wx_access_token.apply_async(countdown=(expire - 1))

@shared_task()
def get_reco_task(accessToken, voiceId):
    return get_complete_voice_reco(accessToken, voiceId)