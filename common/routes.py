from fastapi import APIRouter, Depends

from .configs import settings
from .models import ResponsePayloads

router = APIRouter(tags=["系统设置"])


@router.get(
    "/settings",
    summary="获取站点设置",
    response_model=ResponsePayloads[dict],
)
async def get_site_settings():
    """获取当前站点配置"""
    return ResponsePayloads(data={
        "allow_registration": settings.allow_registration
    })
