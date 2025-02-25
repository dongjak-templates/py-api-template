from pathlib import Path
from typing import List, TypeVar, Optional, Generic

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

T = TypeVar("T")


class Error(BaseModel):
    """表示一个错误

    Attributes:
        type: 错误类型
        message: 错误信息
        code: 错误码

    Author: dongjak
    Created: 2024/11/08
    Version: 1.0
    Since: 1.0
    """

    type: Optional[str] = Field(default=None, description="错误类型")
    message: Optional[str] = Field(default=None, description="错误信息")
    code: Optional[int] = Field(default=None, description="错误码")


class DataPage(BaseModel, Generic[T]):
    """数据分页"""

    items: List[T] = Field(default_factory=list, description="数据项列表")
    total: int = Field(description="总记录数")
    has_more: bool = Field(description="是否有更多数据")


class ResponsePayloads(BaseModel, Generic[T]):
    """响应载荷"""

    data: Optional[T] = Field(default=None, description="数据")
    error: Optional[Error] = Field(default=None, description="错误信息")




class Settings(BaseSettings):
    database_url: str = Field(default=None, description="数据库URL")
    mode: str = Field(default="dev", description="运行模式")
    jwt_secret_key: str = Field(default=None, description="JWT密钥")
    jwt_algorithm: str = Field(default=None, description="JWT算法")
    alipay_appid: str = Field(default="9021000133696987", description="支付宝应用ID")
    alipay_private_key_path: str = Field(
        default=".secrets/app_private_key.sandbox.pem", description="支付宝私钥路径"
    )
    alipay_public_key_path: str = Field(
        default=".secrets/alipay_public_key.sandbox.pem", description="支付宝公钥路径"
    )
    alipay_notify_url: str = Field(
        default="https://notify.cruldra.cn/orders/alipay/notify",
        description="支付宝异步通知URL",
    )
    alipay_return_url: str = Field(
        default="https://return.cruldra.cn/orderStatus",
        description="支付宝同步返回URL",
    )
    alipay_quit_url: str = Field(
        default="http://your-domain.com/orders/alipay/quit",
        description="支付宝中途退出URL",
    )
    alipay_debug: bool = Field(default=True, description="支付宝调试模式")
    wechat_appid: str = Field(default=None, description="微信应用ID")

    wechat_api_key: str = Field(default=None, description="微信API密钥")

    wechat_mch_id: str = Field(default=None, description="微信商户号")

    wechat_key_path: str = Field(default=None, description="微信密钥路径")

    wechat_cert_path: str = Field(default=None, description="微信证书路径")

    wechat_notify_url: str = Field(default=None, description="微信异步通知URL")

    sms_sign_name: str = Field(default=None, description="短信签名")
    sms_template_code: str = Field(default=None, description="短信模板代码")

    # 阿里云访问密钥配置
    aliyun_access_key_id: str = Field(default=None, description="阿里云访问密钥ID")
    aliyun_access_key_secret: str = Field(
        default=None, description="阿里云访问密钥密钥"
    )

    dify_url: str = Field(default=None, description="Dify URL")
    dify_email: str = Field(default=None, description="Dify Email")
    dify_password: str = Field(default=None, description="Dify Password")
    redis_host: str = Field(default=None, description="Redis Host")
    redis_port: int = Field(default=None, description="Redis Port")
    redis_password: str = Field(default=None, description="Redis Password")
    redis_db: int = Field(default=None, description="Redis DB")
    allow_registration: bool = Field(default=True, description="是否允许注册")
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env")
