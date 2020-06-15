from PIL import Image, ImageDraw,ImageFont
from os import path
Image.MAX_IMAGE_PIXELS = None
im = Image.open('G:\BrainSAR_Beta\SAR图片\show.jpg').convert("RGBA")
# x, y = im.size
# try:
#   # 使用白色来填充背景 from：www.jb51.net
#   # (alpha band as paste mask).
#   p = Image.new('RGBA', (500, 500), (205, 0, 0, 0))
#   print(im.size, im.mode)
#   # im.paste(color=(205, 0, 0, 0), box=(1000, 1000, 500, 500), mask='RGBA')
#   im.paste(p, (0, 0))
#   im.show()
#   im.save('G:\BrainSAR_Beta\SAR图片\showgai.png')
# except:
#   pass


# from PIL import Image, ImageDraw,ImageFont
# #将原来的图片转换为RGBA模式
# im = Image.open('G:\BrainSAR_Beta\SAR图片/1.jpg').convert('RGBA')
# #新建一个图片，尺寸与上面的尺寸一样，透明度为0即完全透明
# txt=Image.new('RGBA', im.size, (0,0,0,0))
# #设置要写文字的字体，注意有的字体不能打汉字,这里用的微软雅黑可以
# fnt=ImageFont.truetype("c:/Windows/fonts/msyh.ttc", 30)
# #打汉字
# d=ImageDraw.Draw(txt)
# #写要打的位置，内容,用的字体，文字透明度
# d.text((txt.size[0]-385,txt.size[1]-80),"                     @天之骄子呃\nweibo.com/u/2010089325",font=fnt, fill=(255,255,255,150))
# #两个图片复合
# out=Image.alpha_composite(im, txt)
# #保存加水印后的图片
# out.show()
print(path.dirname('G:\BrainSAR_Beta\SAR图片\show.jpg'))
draw =ImageDraw.Draw(im)
# draw.line((20, 20, 150, 150), 'cyan')
# draw.rectangle((1000, 2000, 300, 400), 'black', 'red')
for i in range(0, 250):
  for j in range(0, 250):
    draw.point((i*2, j*2), fill=(255, 0, 0))

# draw.arc((100, 200, 300, 400), 0, 180, 'yellow')
# draw.ellipse((350, 300, 500, 400), 'yellowgreen', 'wheat')

# font = ImageFont.truetype("consola.ttf", 40, encoding="unic")#设置字
# draw.text((100, 50), u'Hello World', 'fuchsia', font)
#draw.line((0,0) +Image1.size, fill=128)
im.show()