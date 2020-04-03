MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

import redis
from random import choice


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)

    def add(self,proxy,score=INITIAL_SCORE):
        if not self.db.zscore(REDIS_KEY,proxy):
            return self.db.zadd(REDIS_KEY,score,proxy)

    def random(self):
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if  len(result):
            return choice(result)
        else:
            result=self.db.zrangebyscore(REDIS_KEY,0,100)

    def decrease(self,proxy):
        score = self.db.zscore(REDIS_KEY,proxy)
        if score and score>MIN_SCORE:
            print('代理：'+proxy+'当前分数'+score+'-1')
            return self.db.zincrby(REDIS_KEY,proxy,-1)
        else:
            print('当前代理'+proxy+'移除')
            return self.db.zrem(REDIS_KEY,proxy)

