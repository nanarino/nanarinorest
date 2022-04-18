"""一些sqlalchemy.orm的mapper基类"""
from sqlalchemy.orm import registry
from sqlalchemy import Table
from sqlalchemy.schema import CreateTable

# 声明映射
mapper_registry = registry()
Base = mapper_registry.generate_base()
metadata = Base.metadata


def table(mapper: Base) -> Table:
    """表映射声明类 转 表对象"""
    return mapper.__table__


class mapper_to_dict_able_mixin:
    '''混入继承 混入后结果集能直接转化为dict'''

    def keys(self):
        return map(lambda c: c.key, table(self).columns)

    def __getitem__(self, key: str):
        return getattr(self, key)


class create_text_mixin:
    '''混入继承 混入后可以使用__text__获得创表语句'''

    @classmethod
    def __text__(cls) -> CreateTable:
        return CreateTable(table(cls))
