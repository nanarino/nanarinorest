"""一些sqlalchemy.orm的mapper基类"""

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Table
from sqlalchemy.schema import CreateTable
from sqlalchemy.ext.asyncio import AsyncAttrs
from typing import Optional, Iterable


class Base(AsyncAttrs, DeclarativeBase):
    pass


metadata = Base.metadata


def table(mapper: DeclarativeBase | type[DeclarativeBase]) -> Table:
    """表映射声明类 转 表对象"""
    return getattr(mapper, '__table__')


class AsdictableMixin:
    """混入继承 混入后结果集能直接转化为dict"""

    def keys(self) -> Iterable:
        if isinstance(self, Base):
            return map(lambda c: c.key, table(self).columns)
        else:
            return []

    def __getitem__(self, key: str):
        return getattr(self, key)


class CreateDDLMixin:
    """混入继承 混入后可以使用__ddl__获得创表语句"""

    @classmethod
    def __ddl__(cls) -> Optional[CreateTable]:
        if issubclass(cls, Base):
            return CreateTable(table(cls))
