from datetime import datetime
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel
from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Numeric,
    String,
    Integer,
    DateTime,
    Enum as SQLAlchemyEnum,
)
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.postgresql import JSONB


class AssetType(str, Enum):
    APP = "app"
    COURSE = "course"


class DifyAppMode(str, Enum):
    CHAT = "chat"
    AGENT_CHAT = "agent-chat"
    WORKFLOW = "workflow"
    COMPLETION = "completion"


class OrderItem(BaseModel):
    """订单项目"""

    asset_type: AssetType
    asset_id: str
    quantity: int
    unit_price: str


class OrderStatus(str, Enum):
    """订单状态枚举"""

    PENDING = "PENDING"  # 待支付
    PAID = "PAID"  # 已支付
    CANCELLED = "CANCELLED"  # 已取消
    REFUNDED = "REFUNDED"  # 已退款


class PaymentMethod(str, Enum):
    """支付方式枚举"""

    ALIPAY = "alipay"  # 支付宝
    WECHATPAY = "wechatpay"  # 微信支付


class User(SQLModel, table=True):
    """用户信息表"""

    id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, autoincrement=True),
        description="用户ID",
    )
    username: str = Field(
        sa_column=Column(String(50), comment="用户名"), description="用户名"
    )
    phone: str = Field(
        sa_column=Column(String(11), comment="手机号"), description="手机号"
    )
    password: str = Field(
        sa_column=Column(String(100), comment="密码(加密存储)"), description="密码"
    )

    membership_expires: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(), comment="会员到期时间"),
        description="会员到期时间",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime(), comment="创建时间"),
        description="创建时间",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime(), comment="更新时间", onupdate=datetime.now()),
        description="更新时间",
    )
    orders: List["Order"] = Relationship(back_populates="user")
    assets: List["UserAsset"] = Relationship(back_populates="user")
    __table_args__ = {"comment": "用户表"}

    __tablename__ = "qu_users"


class DifyApp(SQLModel, table=True):
    """Dify应用表"""

    id: str = Field(
        default=None,
        sa_column=Column(String, primary_key=True, comment="应用ID"),
        description="应用ID",
    )
    name: str = Field(
        sa_column=Column(String, index=True, comment="名称"), description="名称"
    )
    monthly_price: float = Field(
        default=0.0,
        sa_column=Column(Float, comment="月付价格"),
        description="月付价格",
    )
    yearly_price: float = Field(
        default=0.0,
        sa_column=Column(Float, comment="年付价格"),
        description="年付价格",
    )
    icon_type: Optional[str] = Field(
        default=None,
        sa_column=Column(String, comment="图标类型"),
        description="图标类型",
    )
    icon: Optional[str] = Field(
        default=None, sa_column=Column(String, comment="图标"), description="图标"
    )
    icon_background: Optional[str] = Field(
        default=None,
        sa_column=Column(String, comment="图标背景"),
        description="图标背景",
    )
    icon_url: Optional[str] = Field(
        default=None, sa_column=Column(String, comment="图标URL"), description="图标URL"
    )
    description: str = Field(
        sa_column=Column(String, comment="功能描述"), description="功能描述"
    )
    mode: DifyAppMode = Field(
        sa_column=Column(SQLAlchemyEnum(DifyAppMode), comment="应用模式"),
        description="应用模式",
    )
    api_key: Optional[str] = Field(
        default=None, 
        sa_column=Column(String, index=True, comment="API密钥"),
        description="最后同步的可用API密钥"
    )

    tags: List[str] = Field(
        default=[], sa_column=Column(JSONB, comment="标签列表"), description="标签列表"
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime(), comment="创建时间"),
        description="创建时间",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime(), comment="更新时间", onupdate=datetime.now()),
        description="更新时间",
    )

    __table_args__ = {"comment": "Dify应用表"}
    __tablename__ = "qu_dify_apps"


class Course(SQLModel, table=True):
    """
    课程表
    """

    id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, comment="课程ID"),
        description="ID",
    )

    title: str = Field(
        sa_column=Column(String, index=True, comment="课程标题"), description="课程标题"
    )

    description: str = Field(
        sa_column=Column(String, comment="课程描述"), description="课程描述"
    )

    price: float = Field(sa_column=Column(Float, comment="价格"), description="价格")
    tags: List[str] = Field(
        default=[], sa_column=Column(JSONB, comment="标签列表"), description="标签列表"
    )
    cover_image: Optional[str] = Field(
        default=None,
        sa_column=Column(String, comment="课程封面图片URL"),
        description="课程封面",
    )
    poster_url: Optional[str] = Field(
        default=None,
        sa_column=Column(String, comment="海报图片URL"),
        description="海报图片",
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime(), comment="创建时间"),
        description="创建时间",
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime(), comment="更新时间", onupdate=datetime.now()),
        description="更新时间",
    )
    instructor: Optional[str] = Field(
        default=None, sa_column=Column(String, comment="导师"), description="导师"
    )

    # 添加这一行，建立与章节的关系
    sections: List["CourseSection"] = Relationship(back_populates="course")
    __table_args__ = {"comment": "课程信息表"}
    __tablename__ = "qu_courses"


class CourseSection(SQLModel, table=True):
    """
    课程章节表
    """

    id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, comment="章节ID"),
        description="ID",
    )

    title: str = Field(
        sa_column=Column(String, index=True, comment="章节标题"), description="章节标题"
    )

    duration: int = Field(
        default=0, sa_column=Column(Integer, comment="时长(秒)"), description="时长"
    )

    sort_order: int = Field(
        default=0, sa_column=Column(Integer, comment="排序"), description="排序"
    )

    is_free: bool = Field(
        default=False,
        sa_column=Column(Boolean, comment="是否免费"),
        description="是否免费",
    )

    video_url: Optional[str] = Field(
        default=None, sa_column=Column(String, comment="视频URL"), description="视频URL"
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime(), comment="创建时间"),
        description="创建时间",
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime(), comment="更新时间", onupdate=datetime.now()),
        description="更新时间",
    )

    is_published: bool = Field(
        default=False,
        sa_column=Column(Boolean, comment="是否发布"),
        description="是否发布",
    )

    course_id: int = Field(
        sa_column=Column(Integer, ForeignKey("qu_courses.id"), comment="关联课程ID"),
        description="课程ID",
    )

    course: "Course" = Relationship(back_populates="sections")

    __table_args__ = {"comment": "课程章节表"}
    __tablename__ = "qu_course_sections"


class UserAsset(SQLModel, table=True):
    """用户资产表"""

    id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, autoincrement=True),
        description="资产ID",
    )
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("qu_users.id"), comment="用户ID"),
        description="用户ID",
    )
    asset_type: AssetType = Field(
        default=AssetType.APP,
        sa_column=Column(SQLAlchemyEnum(AssetType), comment="资产类型"),
        description="资产类型",
    )
    app_mode: Optional[DifyAppMode] = Field(
        default=None,
        sa_column=Column(SQLAlchemyEnum(DifyAppMode), comment="应用模式,当资产类型为APP时有效"),
        description="应用模式",
    )
    asset_id: str = Field(
        sa_column=Column(String, comment="资产ID"), description="资产ID"
    )
    asset_name: str = Field(
        sa_column=Column(String, comment="资产名称"), description="资产名称"
    )
    quantity: int = Field(
        default=1,
        sa_column=Column(Integer, comment="数量"),
        description="数量",
    )
    
    expire_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(), comment="有效期至"),
        description="有效期至",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime(), comment="创建时间"),
        description="创建时间",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime(), comment="更新时间", onupdate=datetime.now()),
        description="更新时间",
    )
    user: "User" = Relationship(back_populates="assets")
    __table_args__ = {"comment": "用户资产表"}
    __tablename__ = "qu_user_assets"


class Order(SQLModel, table=True):
    """订单表"""

    id: Optional[str] = Field(
        default=None,
        sa_column=Column(String, primary_key=True, comment="订单ID"),
        description="ID",
    )
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("qu_users.id"), comment="用户ID"),
        description="用户ID",
    )

    amount: float = Field(
        sa_column=Column(Float, comment="订单金额"), description="订单金额"
    )

    status: str = Field(
        default=OrderStatus.PENDING,
        sa_column=Column(
            SQLAlchemyEnum(OrderStatus, name="order_status_enum", native_enum=True),
            comment="订单状态",
        ),
        description="订单状态",
    )
    payment_method: PaymentMethod = Field(
        default=PaymentMethod.ALIPAY,
        sa_column=Column(SQLAlchemyEnum(PaymentMethod), comment="支付方式"),
        description="支付方式",
    )
    pay_time: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(), comment="支付时间"),
        description="支付时间",
    )
    items: List[OrderItem] = Field(
        default=[], sa_column=Column(JSONB, comment="订单项"), description="订单项"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime(), comment="创建时间"),
        description="创建时间",
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime(), comment="更新时间", onupdate=datetime.now()),
        description="更新时间",
    )
    user: "User" = Relationship(back_populates="orders")

    __table_args__ = {"comment": "订单信息表"}
    __tablename__ = "qu_orders"
