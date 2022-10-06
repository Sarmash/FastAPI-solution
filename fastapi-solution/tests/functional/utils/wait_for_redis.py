import time

from aioredis import Redis

if __name__ == "__main__":
    # redis_client = redis.Redis(host="localhost", port=6379, db=0)
    redis_client = Redis("redis://localhost")
    while True:
        if redis_client:
            break
        time.sleep(1)
