"""RESTful API

包括routers schemas

routers都是fastapi.APIRouter实例

"""
__all__ = ['schemas', 'auth', 'card', 'claim']

from . import schemas
from .auth import auth
from .card import card
from .claim import claim
