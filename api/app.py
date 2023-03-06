import asyncio
import logging
import api.exceptions

from fastapi import FastAPI, Depends, Body, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.background import BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, JSONResponse
from api.fetch_article import fetch_article
from api.schemas import HTTPExceptionBody, RequestArticle, ResponseArticle

from api.settings import container_settings
app = FastAPI(
    title=container_settings.service_name,
    version=container_settings.version,
    docs_url='/internal/docs',
    redoc_url=None,
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=container_settings.allowed_origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.exception_handler(exceptions.ExtendedHTTPException)
# async def custom_http_exception_handler(request, exc: exceptions.ExtendedHTTPException):
#     content = jsonable_encoder(exc, exclude_none=True, exclude={'status_code'})
#     logging.info(f" {exc.__class__.__name__}: {content}")
#     return JSONResponse(content=content, status_code=exc.status_code)


# @app.exception_handler(RequestValidationError)
# async def logging_validation_exception_handler(request, exc: RequestValidationError):
#     logging.info(f"The client sent invalid data!: {exc}\nClient data: {exc.body}")
#     return await request_validation_exception_handler(request, exc)


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
async def load_article_xlsx(request: RequestArticle) -> ResponseArticle:
    article = await fetch_article(request)
    return article

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