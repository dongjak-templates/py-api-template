# 简介

{{PROJECT_NAME}}


## 技术栈

- `Python`
- `FastAPI`
- `SQLModel`
- `Uvicorn`
- `Alembic`

# 部署

## 数据库

```bash
alembic revision --autogenerate -m "update course model"
```

```bash
alembic upgrade head
```

## 构建镜像

```bash
docker build --no-cache -t asm-py:latest .
```