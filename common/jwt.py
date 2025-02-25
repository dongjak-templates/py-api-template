from datetime import timedelta, datetime
from typing import Optional

import jwt

from .configs import settings


def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    # 添加过期时间
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=365)

    to_encode.update({"exp": expire})

    # 添加发布时间
    to_encode.update({"iat": datetime.utcnow()})

    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt