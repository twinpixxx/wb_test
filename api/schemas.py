from uuid import UUID

from pydantic import BaseModel


class RequestArticle(BaseModel):
    article: str


class ResponseArticle(BaseModel):
    article: str
    brand: str
    title: str


class HTTPExceptionBody(BaseModel):
    detail: str