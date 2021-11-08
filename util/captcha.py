from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from random import choice, randint
import base64


def create_char() -> str:
    """生成随机4个数组或字母"""
    char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join([choice(char) for i in range(4)])


def create_img():
    '''返回元组 key，img'''
    text = create_char()
    image = Image.new("RGB", (100, 50), (124, 231, 122))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./util/captcha.ttf', size=30)
    x = 15
    for i in text:  # 随机验证码
        # 随机深色
        R = str(randint(0, 176))
        G = str(randint(0, 160))
        B = str(randint(0, 176))

        draw.text((x, 10), text=i, font=font,
                  fill=f"rgb({R},{G},{B})", direction=None)

        x += 20

    # 添加干扰线条
    for i in range(1, randint(7, 15)):  # 线条数量在7-15间
        x, y = randint(0, 100), randint(0, 50)  # 线条起点
        x2, y2 = randint(0, 100), randint(0, 50)  # 线条终点
        # 随机浅色
        R = str(randint(192, 255))
        G = str(randint(192, 243))
        B = str(randint(192, 255))
        # 绘制线条 宽度为2
        draw.line((x, y, x2, y2), fill=f"rgb({R},{G},{B})", width=2)

    output_buffer = BytesIO()
    # image.show()
    image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf8')
    return text, 'data:image/jpeg;base64,' + base64_str
