from celery import shared_task
from src.service.summary import save_by_userid

@shared_task
def save_by_userid_task(content, userid):
    print("userID")
    print(userid)
    return save_by_userid(userid=userid, content=content)