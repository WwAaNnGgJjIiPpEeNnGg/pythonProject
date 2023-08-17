import random
from PIL import Image, ImageDraw, ImageFont


# 生成随机验证码
def generate_random_code(length=6):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


# 创建验证码图像
def create_code_image(code, width=200, height=100):
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 36)
    draw.text((10, 40), code, fill=(0, 0, 0), font=font)
    return image


# 主程序
def main():
    correct_code = generate_random_code()
    image = create_code_image(correct_code)
    image.show()

    user_input = input("请输入验证码：")
    if user_input == correct_code:
        print("验证通过！")
    else:
        print("验证失败！")


if __name__ == "__main__":
    main()
