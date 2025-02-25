"""
BCrypt 密码加密工具
"""
import bcrypt


class BCryptPasswordEncoder:
    """BCrypt 密码加密器"""

    def __init__(self, strength: int = 10):
        """
        初始化加密器
        :param strength: 加密强度（轮数），默认为10
        """
        self.strength = strength

    def encode(self, raw_password: str) -> str:
        """
        加密密码
        :param raw_password: 原始密码
        :return: 加密后的密码
        :raises ValueError: 如果密码为空
        """
        if not raw_password:
            raise ValueError('Password cannot be null')
        
        # bcrypt 需要 bytes 类型的输入
        password_bytes = raw_password.encode('utf-8')
        # 生成盐值并加密
        salt = bcrypt.gensalt(rounds=self.strength)
        hashed = bcrypt.hashpw(password_bytes, salt)
        # 返回字符串形式的哈希值
        return hashed.decode('utf-8')

    def matches(self, raw_password: str, encoded_password: str) -> bool:
        """
        验证密码

        Args:
            raw_password: 原始密码
            encoded_password: 加密后的密码
            
        Returns:
            是否匹配
        """
        if not raw_password or not encoded_password:
            return False

        try:
            # 将输入转换为 bytes
            raw_bytes = raw_password.encode('utf-8')
            encoded_bytes = encoded_password.encode('utf-8')
            # 验证密码
            return bcrypt.checkpw(raw_bytes, encoded_bytes)
        except (ValueError, TypeError):
            return False

    def upgrade_encoding(self, encoded_password: str) -> bool:
        """
        检查是否需要升级加密强度
        :param encoded_password: 已加密的密码
        :return: 是否需要升级
        """
        if not encoded_password:
            return False

        try:
            rounds = self.get_rounds(encoded_password)
            return rounds != self.strength
        except ValueError:
            return True

    def get_rounds(self, encoded_password: str) -> int:
        """
        获取加密轮数
        :param encoded_password: 已加密的密码
        :return: 加密轮数
        :raises ValueError: 如果加密的密码为空或格式不正确
        """
        if not encoded_password:
            raise ValueError('Encoded password cannot be null')

        try:
            # bcrypt 哈希的格式为 $2b$XX$...，其中 XX 是轮数
            parts = encoded_password.split('$')
            if len(parts) >= 3:
                return int(parts[2])
            raise ValueError('Invalid hash format')
        except (IndexError, ValueError) as e:
            raise ValueError('Invalid hash format') from e


# 创建一个默认的加密器实例
default_password_encoder = BCryptPasswordEncoder()