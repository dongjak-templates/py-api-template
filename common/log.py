import sys
from pathlib import Path

from loguru import logger

from .configs import settings


def configure_logger():
    """配置日志"""

    # 项目根目录
    project_root = Path(__file__).parent.parent

    # 日志文件路径
    log_path = project_root / ".logs"
    log_path.mkdir(exist_ok=True)

    # 移除默认处理器
    logger.remove()
    level = "DEBUG" if settings.mode == "dev" else "INFO"
    # 添加控制台处理器 (开发环境)
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
        level=level,
        enqueue=True,
    )

    # 添加文件处理器 (INFO级别)
    logger.add(
        log_path / "info.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=level,
        rotation="1 day",  # 每天轮转
        retention="30 days",  # 保留30天
        compression="zip",  # 压缩
        enqueue=True,
    )

    # 添加文件处理器 (ERROR级别)
    logger.add(
        log_path / "error.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="1 day",
        retention="30 days",
        compression="zip",
        enqueue=True,
    )

    # 智能体相关的日志
    logger.add(
        log_path / "agents.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        filter=lambda record: record.get("extra", {}).get("name") == "agents",
        rotation="1 day",
        level=level,
        retention="30 days",
        compression="zip",
        enqueue=True,
    )
    # 添加聊天相关的日志处理器
    logger.add(
        log_path / "chat.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        filter=lambda record: record.get("extra", {}).get("name") == "chat",
        rotation="1 day",  # 每天轮转
        level=level,
        retention="30 days",  # 保留30天
        compression="zip",  # 压缩
        enqueue=True,
    )
    # 添加支付相关的日志处理器
    logger.add(
        log_path / "payment.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        filter=lambda record: record.get("extra", {}).get("name") == "payment",
        rotation="1 day",  # 每天轮转
        level=level,
        retention="30 days",  # 保留30天
        compression="zip",  # 压缩
        enqueue=True,
    )

    return logger


configure_logger()
payment_logger = logger.bind(name="payment")
agents_logger = logger.bind(name="agents")
chat_logger = logger.bind(name="chat")
