# from fastapi import HTTPException
# import redis.asyncio as redis
# from api.schemas import ResponseArticle

# from api.settings import ContainerSettings


# async def is_cached(article: str) -> bool:
#     connection = await redis.from_url(ContainerSettings.redis_dsn, decode_responses=True)

#     value = await connection.get(name=article)
#     if value is None:
#         raise HTTPException(status_code=401, detail="Refresh token not found")

#     return True


# async def get_from_cache(article: str) -> ResponseArticle:
#     connection = await redis.from_url(ContainerSettings.redis_dsn, decode_responses=True)

#     value = await connection.get(name=article)

#     return ResponseArticle(**value)

