"""RESTful API

包括routers schemas

routers都是fastapi.APIRouter实例

"""
__all__ = ['schemas', 'demo', 'auth']

from . import schemas
from .demo import demo
from .auth import auth
