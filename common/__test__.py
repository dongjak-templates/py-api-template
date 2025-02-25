from .sms import sms_service


def test_send_sms_success():
    """测试发送短信成功的情况"""
    # 准备测试数据
    phone_number = "13271976859"
    template_param = {"code": "1234"}

    # 发送短信
    result = sms_service.send_sms(phone_number, template_param)
    assert result is True