"""一些sqlalchemy.orm的mapper基类"""
from sqlalchemy.orm import registry
from sqlalchemy import Table, Column
from sqlalchemy.schema import CreateTable
from typing import NewType, Optional, Iterable

# 声明映射
mapper_registry = registry()
Base = mapper_registry.generate_base()
Model = NewType('Model', Base)
metadata = Base.metadata


def table(mapper: Model | type[Model]) -> Table:
    """表映射声明类 转 表对象"""
    return mapper.__table__


class mapper_to_dict_able_mixin():
    '''混入继承 混入后结果集能直接转化为dict'''

    def keys(self) -> Iterable:
        if isinstance(self, Base):
            return map(lambda c: c.key, table(self).columns)
        else:
            return []

    def __getitem__(self, key: str):
        return getattr(self, key)


class create_ddl_mixin():
    '''原定为混入继承 混入后可以使用__ddl__获得创表语句'''

    @classmethod
    def __ddl__(cls) -> Optional[CreateTable]:
        if issubclass(cls, Base):
            return CreateTable(table(cls))
