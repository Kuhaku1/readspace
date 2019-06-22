# -*- coding: utf-8 -*-
# Author:李星宇
import redis
import os
__all__ = ['redislinktool']

REDIS_SERVER_ADDRESS = os.environ.get("REDIS_SERVER_ADDRESS", "localhost")

redislinktool = redis.Redis(REDIS_SERVER_ADDRESS, 6379, 5)
