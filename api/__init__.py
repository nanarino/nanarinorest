"""RESTful API

包括routers schemas

routers都是fastapi.APIRouter实例
依赖orm和jwt等目录的代码

"""
__all__ = ['schemas', 'demo', 'auth']

from . import schemas
from .demo import demo
from .auth import auth
