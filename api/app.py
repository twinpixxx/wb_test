import api.exceptions

from fastapi import FastAPI, File, Response, UploadFile
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from api.fetch_article import fetch_article
from api.schemas import HTTPExceptionBody, RequestArticle, ResponseArticle

from api.settings import container_settings
from api.utils import parse_xlsx


app = FastAPI(
    title=container_settings.service_name,
    version=container_settings.version,
    docs_url='/internal/docs',
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=container_settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/article",
          responses={
                200: {"model": ResponseArticle},
                401: {"model": HTTPExceptionBody},
                404: {"model": api.exceptions.ArticleNotFound},
          })
async def load_article(request: RequestArticle) -> ResponseArticle:
    article = await fetch_article(request)
    return article


@app.post("/api/v1/article/xlsx",
          responses={
                200: {"model": ResponseArticle},
                401: {"model": HTTPExceptionBody},
                404: {"model": api.exceptions.ArticleNotFound},
          })
async def load_article_xlsx(file: UploadFile = File(...)) -> list[ResponseArticle]:
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    finally:
        file.file.close()

    articles = parse_xlsx(file.filename)
    response = []

    for article in articles:
       response.append(await fetch_article(RequestArticle(article=article)))
    return response

"""General functionality"""


@app.get("/", tags=["public"])
async def index():
    return Response(
        content=f"""<head><title>{container_settings.service_name}</title></head><body><h1>{container_settings.service_name} {container_settings.service_version}</h1><h4 style="color: {get_docs_color(container_settings.environment_name)}">environment: {container_settings.environment_name}</h4><a href='/docs'>Docs</a></body>""",
        media_type="text/html")


@app.get("/docs", tags=["public"])
async def docs_redirect():
    return RedirectResponse(url='/internal/docs')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('internal:app', host=container_settings.web_host, port=container_settings.web_port, reload=container_settings.autoreload)