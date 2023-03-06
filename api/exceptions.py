from dataclasses import dataclass

from starlette import status


@dataclass
class ExtendedHTTPExceptionBody:
    detail: str  # human readable description
    error_code: str  # error code as string enum
    additional_info: str = None  # additional info for debugging


class ExtendedHTTPException(ExtendedHTTPExceptionBody, Exception):
    status_code: int  # HTTP status code

    def __init__(self, detail: str = None, additional_info: str = None) -> None:
        if detail is not None:
            self.detail = detail
        self.additional_info = additional_info


class ArticleNotFound(ExtendedHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Article not found'
    error_code = 'article_not_found'