import redis
from src.settings import settings

redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)