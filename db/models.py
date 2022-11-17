"""数据表映射"""
from .base import Base, mapper_to_dict_able_mixin, create_ddl_mixin
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DateTime


class Demo(mapper_to_dict_able_mixin, create_ddl_mixin, Base):
    __tablename__ = 'demo'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    type = Column(String(255))
    mark = Column(String(255))
    create_at = Column(DateTime)
    is_active = Column(Integer)


class User(mapper_to_dict_able_mixin, create_ddl_mixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(63))
    password = Column(String(63))
