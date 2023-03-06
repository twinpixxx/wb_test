import json
from fastapi import HTTPException
import redis
from api.schemas import ResponseArticle

from api.settings import container_settings


def is_cached(article: str) -> bool:
    connection = redis.from_url(container_settings.redis_dsn, decode_responses=True)

    value = connection.get(name=article)
    
    if value is None:
        return False

    return True


def get_from_cache(article: str) -> ResponseArticle:
    connection = redis.from_url(container_settings.redis_dsn, decode_responses=True)

    value = json.loads(connection.get(name=article))

    return ResponseArticle(**value)


def save_to_cache(article: str, payload: ResponseArticle) -> None:
    connection = redis.from_url(container_settings.redis_dsn, decode_responses=True)
    connection.set(
        name=article,
        value=payload.json(),
    )
