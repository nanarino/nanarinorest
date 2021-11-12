"""数据表映射"""
from sqlalchemy.sql.functions import user
from .base import Base, mapper_to_dict_able_mixin
from sqlalchemy import Column
from sqlalchemy.types import Integer, String


class Card(mapper_to_dict_able_mixin, Base):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    username = Column(String(63))
    password = Column(String(63))
    is_active = Column(Integer)


class Card_bindinfo(mapper_to_dict_able_mixin, Base):
    __tablename__ = "card_bindinfo"
    id = Column(Integer, primary_key=True)
    cid = Column(Integer)
    tbr_name = Column(String(255))
    tbr_id_type = Column(String(255))
    tbr_id_num = Column(String(255))
    tbr_sex = Column(String(255))
    tbr_birth = Column(String(255))
    tbr_age = Column(Integer)
    tbr_email = Column(String(255))
    tbr_tel = Column(String(255))
    tbr_addr = Column(String(255))
    bbr_is_tbr = Column(String(255))
    bbr_name = Column(String(255))
    bbr_id_type = Column(String(255))
    bbr_id_num = Column(String(255))
    bbr_sex = Column(String(255))
    bbr_birth = Column(String(255))
    bbr_age = Column(Integer)
    bbr_email = Column(String(255))
    bbr_tel = Column(String(255))
    bbr_addr = Column(String(255))
    effect_date = Column(String(255))
