from aioredis import Redis

redis: Redis = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    return redis
