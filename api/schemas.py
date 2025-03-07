"""请求响应所需的类型注释 以及作为fastapi docs的schema"""

from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class msg(BaseModel):
    """操作成功(?)的消息返回"""

    msg: str
    id: Optional[int] = None


class sliced[T: BaseModel](BaseModel):
    """分页的T数据"""

    total: int
    slice_data: list[T]


class meta_data(BaseModel):
    """通用元数据"""

    id: int
    create_at: datetime


class demo_data(BaseModel):
    """创建需要的demo数据"""

    name: str
    type: str
    mark: str


class demo(demo_data, meta_data):
    pass


class demos_sliced(sliced[demo]):
    pass


class user(meta_data):
    """用户数据"""

    username: str
    password: str


class auth_token_data(BaseModel):
    """jwt数据。

    无法覆盖签发者iss，因为它读取配置文件
    无法覆盖超时信息exp，因为它读取配置文件或者encode的timeout参数
    不应包含sub等信息 会被特殊处理甚至解析不了
    """

    uid: int
    uname: str
    exp: int = 0
    iss: str = ''


class auth_res(BaseModel):
    """auth授权表单返回数据"""

    access_token: str
    token_type: str = 'bearer'


if __name__ == '__main__':
    pass
