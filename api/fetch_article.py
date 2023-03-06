import asyncio
import json
import httpx
from api.exceptions import ArticleNotFound
from api.redis_helpers import get_from_cache, is_cached, save_to_cache
from api.schemas import RequestArticle, ResponseArticle


async def fetch_article(article_request: RequestArticle) -> ResponseArticle:

    article = json.loads(article_request.json())['article']
    if is_cached(article):
        print('from cache')
        return get_from_cache(article)
    
    async with httpx.AsyncClient() as client:
        tasks = []

        for number in range(1, 11):
            basket = f"basket-{number:02d}"
            vol = f"vol{article[0:3] if len(article) == 8 else article[0:4]}"
            part = f"part{article[0:5] if len(article) == 8 else article[0:6]}"
            api_url = f'https://{basket}.wb.ru/{vol}/{part}/{article}/info/ru/card.json'

            tasks.append(client.get(api_url))

        result = await asyncio.gather(*tasks)
        for r in result:
            if r.status_code == 200:
                data = r.json()
                brand = data['selling']['brand_name']
                title = f"{brand} / {data['imt_name']}"

                response = ResponseArticle(
                    article=article,
                    brand=brand,
                    title=title)
                
                save_to_cache(article=article, payload=response)

                return response

    raise ArticleNotFound
