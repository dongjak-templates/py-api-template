import uvicorn
from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager

import common
from common import ResponsePayloads, Error


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # 启动时执行
#     dify.TokenManager.start_scheduler()
#     yield
#     # 关闭时执行（可留空）


app = FastAPI(
    # lifespan=lifespan,  # 添加生命周期管理
    title="AI智元API文档",
    description="包含课程和智能体",
    version="1.0.0",
    servers=[{"url": "http://localhost:8000", "description": "本地开发环境"}],
)


@app.exception_handler(Exception)
async def api_exception_handler(request: Request, exc):
    """处理自定义API异常"""
    return JSONResponse(
        status_code=500,
        content=ResponsePayloads(
            error=Error(type=type(exc).__name__, message=str(exc), code=500)
        ).model_dump(),
    )


# 1. 自定义未授权异常处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return JSONResponse(
            status_code=exc.status_code,
            content=ResponsePayloads(
                data=None,
                error=Error(type="Unauthorized", message=exc.detail, code=exc.status_code),
            ).model_dump(),
        )
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponsePayloads(
            data=None,
            error=Error(type="HTTPException", message=exc.detail, code=exc.status_code),
        ).model_dump(),
    )


@app.exception_handler(StarletteHTTPException)
async def not_found_exception_handler(request: Request, exc: StarletteHTTPException):
    """处理404等HTTP异常"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponsePayloads(
            error=Error(
                type="NotFound" if exc.status_code == 404 else type(exc).__name__,
                message=str(exc.detail),
                code=exc.status_code,
            )
        ).model_dump(),
    )


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:1420", "https://return.cruldra.cn"],
#     allow_methods=["*"],
#     allow_headers=["*"],
#     allow_credentials=True,
#     expose_headers=["*"],
#     max_age=3600,
# )

# app.include_router(users.router)
# app.include_router(orders.router)
# app.include_router(dify.router)
# app.include_router(courses.router)
# app.include_router(common.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
