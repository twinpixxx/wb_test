import logging

import pydantic
from fastapi import APIRouter
from api.app import app
from api.settings import container_settings

logging.basicConfig(level=container_settings.logging_level)
logger = logging.getLogger(__name__)


class CheckFail(pydantic.BaseModel):
    componentType: str
    status = 'fail'
    output: str


class CheckOk(pydantic.BaseModel):
    componentType: str | None = None
    status = 'pass'


class RFCHealthDraft(pydantic.BaseModel):
    status: str
    checks: dict[str, list[CheckFail | CheckOk]]


internal_router = APIRouter(prefix='/internal', tags=['internal'])


@internal_router.get('/health')
async def health():
    return RFCHealthDraft(
        status='pass',
        checks={
            "App": [
                CheckOk()
            ]
        }
    ).dict(exclude_none=True)


app.include_router(internal_router)