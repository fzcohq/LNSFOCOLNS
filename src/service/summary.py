from src.db.redis import redis_instance

def save_by_userid(userid, content):
    redis_instance.rpush(str(userid), content)

def get_by_userid(userid):
    return redis_instance.lrange(userid, 0, -1)