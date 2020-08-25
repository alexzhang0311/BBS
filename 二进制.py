# #0b开头代表为二进制
#
# a = 0b00000001
# b = 0b00100000
# print(a,a&b)
#
# #判断某个用户有没有某个权限A：
# #将需要对比的用户权限和A权限的二进制码进行与运算，如果得到的结果和A相等，那么代表用户有A权限，否则代表没有
#
from utils import cache

cache.set(key='email',value='alex')
# print(cache.get(key='amos@hk.chinamobile.com'))
print(cache.get(key='92047291'))


# import string,random
# SOURCE = list(string.ascii_letters)
# for index in range(0, 10):
#     SOURCE.append(str(index))
#
#
# text = random.sample(SOURCE,5)
#
# text1 = ''.join(text)


# from PIL import Image,ImageDraw,ImageFont
# font = ImageFont.truetype('utils/captcha/segoeuib.ttf',25)
# font_width, font_height = font.getsize(text1)
# image = Image.new('RGBA',(100,30),(255,0,255))
# draw = ImageDraw.Draw(image)
# # draw.text(((100 - font_width) / 2, (30 - font_height) / 2),text1,font=font,fill=(0,0,0))
# draw.text((20,-5),text1,font=font,fill=(0,0,0))
# print(text1)
# with open('test.png','wb') as fp:
#     image.save(fp)

# fonts = [
#             'Courgette-Regular.ttf',
#             'segoeuib.ttf',
#             'verdana.ttf',
#             'verdanab.ttf',
#             'verdanai.ttf',
#             'verdanaz.ttf'
#         ]
# font = random.choice(fonts)
# print('utils/captcha/' + font)


print('hello world')