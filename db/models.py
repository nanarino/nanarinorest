"""数据表映射"""
from .base import Base, AsdictableMixin, CreateDDLMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, String, DateTime
from datetime import datetime


class Demo(AsdictableMixin, CreateDDLMixin, Base):
    __tablename__ = 'demo'
    id :Mapped[int] = mapped_column(Integer, primary_key=True)
    name :Mapped[str] = mapped_column(String(255))
    type :Mapped[str] = mapped_column(String(255))
    mark :Mapped[str] = mapped_column(String(255))
    create_at :Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    is_active :Mapped[int] = mapped_column(Integer, default=1)


class User(AsdictableMixin, CreateDDLMixin, Base):
    __tablename__ = 'user'
    id :Mapped[int] = mapped_column(Integer, primary_key=True)
    username :Mapped[str] = mapped_column(String(63))
    password :Mapped[str] = mapped_column(String(63))
