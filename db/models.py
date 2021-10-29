"""数据表映射"""
from .base import Base, mapper_to_dict_able_mixin
from sqlalchemy import Column
from sqlalchemy.types import Integer, String


class Demo(mapper_to_dict_able_mixin, Base):
    __tablename__ = 'demotable'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class User(mapper_to_dict_able_mixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(63))
    password = Column(String(63))