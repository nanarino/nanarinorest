"""请求响应所需的类型注释 以及作为fastapi docs的schema"""
from pydantic import BaseModel


class card(BaseModel):
    id: int
    is_active: int = 0
    username: str
    password: str


class auth_token_data(BaseModel):
    '''jwt数据。 

    无法覆盖签发者iss，因为它读取配置文件
    无法覆盖超时信息exp，因为它读取配置文件或者ecd的timeout参数
    不应包含sub等信息 会被特殊处理甚至解析不了
    '''
    cid: int
    uname: str
    exp: int = 0
    iss: str = ''


class auth_res(BaseModel):
    """auth授权表单返回数据"""
    access_token: str
    token_type: str = "bearer"


class auth_captcha(BaseModel):
    """请求验证码图片返回数据"""
    captcha_token: str
    captcha_img: str


class card_bindinfo(BaseModel):
    tbr_name: str
    tbr_id_type: str
    tbr_id_num: str
    tbr_sex: str
    tbr_birth: str
    tbr_age: int
    tbr_email: str
    tbr_tel: str
    tbr_addr: str
    bbr_is_tbr: str
    bbr_name: str
    bbr_id_type: str
    bbr_id_num: str
    bbr_sex: str
    bbr_birth: str
    bbr_age: int
    bbr_email: str
    bbr_tel: str
    bbr_addr: str
    effect_date: str


if __name__ == '__main__':
    try:
        print(auth_token_data(**{'uname': 1}))
    except Exception as e:
        print(type(e))
