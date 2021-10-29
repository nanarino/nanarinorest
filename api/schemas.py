"""请求响应所需的类型注释 以及作为fastapi docs的schema"""
from pydantic import BaseModel


class demo(BaseModel):
    id: int
    name: str


class demos_sliced(BaseModel):
    total: int
    slice_data: list[demo]


class user(BaseModel):
    id: int
    username: str
    password: str


class auth_token_data(BaseModel):
    '''jwt数据。 

    无法覆盖签发者iss，因为它读取配置文件
    无法覆盖超时信息exp，因为它读取配置文件或者ecd的timeout参数
    不应包含sub等信息 会被特殊处理甚至解析不了
    '''
    uid: int
    uname: str
    exp: int = 0
    iss: str = ''


class auth_res(BaseModel):
    """auth授权表单返回数据"""
    access_token: str
    token_type: str = "bearer"


if __name__ == '__main__':
    try:
        print(auth_token_data(**{'uname':1}))
    except Exception as e:
        print(type(e))
