from typing import Dict, Optional

from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_dysmsapi20170525.models import SendSmsRequest
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions

from .configs import settings
from .log import logger


class SMSService:
    """短信服务类
    
    用于发送阿里云短信服务
    """

    def __init__(self):
        """初始化短信服务客户端"""
        config = Config(
            access_key_id=settings.aliyun_access_key_id,
            access_key_secret=settings.aliyun_access_key_secret,
            endpoint='dysmsapi.aliyuncs.com'
        )
        self.client = Client(config)

    def send_sms(self, phone_number: str, template_param: Optional[Dict] = None) -> bool:
        """发送短信
        
        Args:
            phone_number: 手机号码
            template_param: 模板参数，例如 {"code": "1234"}
            
        Returns:
            bool: 发送是否成功
        """
        try:
            request = SendSmsRequest(
                phone_numbers=phone_number,
                sign_name=settings.sms_sign_name,
                template_code=settings.sms_template_code,
                template_param=str(template_param) if template_param else None
            )

            runtime = RuntimeOptions()
            response = self.client.send_sms_with_options(request, runtime)

            if response.body.code == "OK":
                logger.info(f"短信发送成功: {phone_number}")
                return True
            else:
                logger.error(f"短信发送失败: {response.body.message}")
                return False

        except Exception as e:
            logger.error(f"短信发送异常: {str(e)}")
            return False


# 创建全局短信服务实例
sms_service = SMSService()
