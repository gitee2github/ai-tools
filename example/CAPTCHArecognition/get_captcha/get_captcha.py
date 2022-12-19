import os
import math
import random
from time import time
from captcha.image import ImageCaptcha
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from images_spider import BingImagesSpider

#-----------------------------------------------
#   character类的验证码生成
#-----------------------------------------------
# 模型只支持识别[4, 5, 6]位验证码
class GetCaptcha():
    def __init__(self, fonts=None, font_sizes=None):
        self.fonts = fonts
        self.font_sizes = font_sizes

    def Unicode(self):
        val = random.randint(0x4e00, 0x9fbf)
        return chr(val)

    def get_base(self, save_path, cap_array_d, num=4, num_img=1):
        # cap_val : 指定验证码中的内容，但不过过长
        assert num in [4, 5, 6]
        image = ImageCaptcha(fonts=self.fonts, font_sizes=self.font_sizes)
        for i in range(num_img):
            assert len(cap_array_d) > 0
            cap_val  = "".join(random.sample(cap_array_d, num))
            image_name = "{}_{}.png".format(cap_val,i)
            print(image_name)
            image.write(cap_val, os.path.join(save_path,image_name))

    def get_number_and_letter(self, save_path, num=4, num_img=1):
        self.get_base(save_path,list("0123456789abcdefghijklmnopqrstuvwxyz"), num, num_img)

    def get_pure_letter(self, save_path, num=4, num_img=1):
        self.get_base(save_path,list("abcdefghijklmnopqrstuvwxyz"), num, num_img)

    def get_pure_number(self, save_path, num=4, num_img=1):
        self.get_base(save_path,list("0123456789"), num, num_img)

#-----------------------------------------------
#   数学运算类的验证码生成（+、-、x）
#----------------------------------------------- 
def get_number_operations(save_path, num_img = 1):
    font_file = 'DroidSansMono.ttf'
    font_size = 42
    char_length = 3
    width = 160
    height = 60 

    def rndColor():
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))
    
    # 写文字
    font = ImageFont.truetype(font_file,font_size)
    for i in range(num_img):
        img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img, mode='RGB')
        operation = random.sample(['+','-','x'], 1)[0]
        if operation == '-':
            a = random.randint(1,20)
            b = random.randint(1,20)
            h = random.randint(0,5)
            draw.text([0 * width / char_length, h], str(a+b), font=font, fill=rndColor())
            draw.text([1 * width / char_length, h], '-', font=font, fill=rndColor())
            draw.text([2 * width / char_length, h], str(a), font=font, fill=rndColor())
            write_name = str(i)+'_'+str(a+b)+'S'+str(a)+'.png'
        else:
            a = str(random.randint(1,20))
            b = str(random.randint(1,20))
            h = random.randint(0, 4)
            draw.text([0 * width / char_length, h], a, font=font, fill=rndColor())
            draw.text([1 * width / char_length, h], operation, font=font, fill=rndColor())
            draw.text([2 * width / char_length, h], b, font=font, fill=rndColor())
            write_name = str(i)+'_'+str(a)+('X' if operation=='x' else 'A')+str(b)+'.png'

        # 写干扰点
        for i in range(40):
            draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
    
        # 写干扰圆圈
        for i in range(40):
            draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())
    
        # 画干扰线
        for i in range(5):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
    
            draw.line((x1, y1, x2, y2), fill=rndColor())
 
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        img.save(os.path.join(save_path,write_name))
        print(write_name)

#-----------------------------------------------
#   滑块拖拽类的验证码生成
#-----------------------------------------------
def get_behavior_drag(save_path, num_captcha=1):
    background_ = Image.open('behavior/behavior_drag/background.png')
    shape_block = Image.open('behavior/behavior_drag/shape.png').convert('RGBA')
    assert shape_block.height <= background_.height # 随机上下位置
    ranglen = background_.width - 2 * shape_block.width
    for n in range(num_captcha):
        background = background_.copy()
        shape = Image.new(mode='RGBA', size=(shape_block.width, background.height), color=(0, 0, 0, 0))
        hig = random.randint(0,background.height-shape_block.height)
        pos = shape.width + random.randint(10,ranglen)
        ans = (pos+shape_block.width//2, hig+shape_block.height//2)
        shape.paste(shape_block, (0, hig))
        shape_back_pixel = shape.getpixel((0,0))
        for i in range(0, shape.width):
            for j in range(0,shape.height):
                pixel = shape.getpixel((i,j))
                if pixel == shape_back_pixel:
                    continue
                back_pixel = background.getpixel((pos+i,j))
                pixel = list(pixel)
                back_pixel = list(back_pixel)
                pixel[0] = back_pixel[0]
                pixel[1] = back_pixel[1]
                pixel[2] = back_pixel[2]
                shape.putpixel((i,j),tuple(pixel))
                alpha = pixel[3] * 1.0 / 0xff
                back_pixel[0] = int((1 - alpha) * back_pixel[0] + alpha * 0xff)
                back_pixel[1] = int((1 - alpha) * back_pixel[1] + alpha * 0xef)
                back_pixel[2] = int((1 - alpha) * back_pixel[2] + alpha * 0xdb)
                back_pixel[3] = int((0xff * 0xff - (0xff - back_pixel[3])) / 0xff)
                background.putpixel((pos+i,j),tuple(back_pixel))

        background.save(os.path.join(save_path,'back_{}_pw{}_ph{}.png'.format(n,ans[0],ans[1])),'PNG')
        shape.save(os.path.join(save_path,'shape_{}_pw{}_ph{}.png'.format(n,ans[0],ans[1])),'PNG')
        print('behavior_drag captcha {} completed.'.format(n))

#-----------------------------------------------
#   图片旋转类的验证码生成
#-----------------------------------------------
def get_behavior_rotate(input_img_path, save_path, num_captcha=1):
    img = Image.open(input_img_path).convert('RGBA')
    r = min(img.height,img.width)//2
    c = [img.width//2,img.height//2]
    for i in range(img.width):
        for j in range(img.height):
            if (i-c[0])**2 + (j-c[1])**2 < r**2:
                continue
            img.putpixel((i,j),tuple((0,0,0,0)))
    for n in range(num_captcha):
        img_ = img.copy()
        ro   = random.randint(10,350)
        # rotated the given number of degrees counter clockwise around its centre
        img_ = img_.rotate(ro)
        name = os.path.split(input_img_path)[-1][:-4]
        img_.save(os.path.join(save_path,name+'_ro_{}.png'.format(ro)),'PNG')
        print('behavior_rotate captcha {} completed.'.format(n))

#-----------------------------------------------
#   物体识别类的验证码生成（九宫格点选）
#   input_img_path图片路径
#   object_pos目标物体的位置（用来给出验证码的真值）list[[x1,y1],...]
#-----------------------------------------------
def get_behavior_object_recognition(input_img_path, object_pos, save_path):
    image = Image.open(input_img_path)
    name = os.path.split(input_img_path)[-1][:-4]
    # 九宫格裁剪
    width, height = image.size
    item_width = int(width / 3)
    item_height = int(height / 3)
    box_list = []
    ans = []
    # (left, upper, right, lower)
    print('waiting...')
    for i in range(0,3):
        for j in range(0,3):
            box = (j*item_width,i*item_height,(j+1)*item_width,(i+1)*item_height)
            count = 0
            for ii in range(box[0],box[2]):
                for jj in range(box[1],box[3]):
                    if is_in_2d_polygon([ii,jj], object_pos): count += 1

            ans.append(count > 10)
            box_list.append(box)
            image_list = [image.crop(box) for box in box_list]
  
    #保存图片 
    index = 1
    for image in image_list: 
        image.save(os.path.join(save_path,name+'_'+str(index)+('_t' if ans[index-1] else '_f')+'.png'), 'PNG')
        index += 1

    print(os.path.split(input_img_path)[-1]+' : save completed!')


'''
@description 判断点point是否在由顶点数组vertices所指定的多边形内部
思想：将点point和多边形所有的顶点链接起来，计算相邻两边的夹角之和，
若和等于360°，那说明该点就在多边形内。
参考链接：http://www.html-js.com/article/1538
@param  point 待判断的点。有两个分量的List。
@param  vertices 多边形顶点数组，其中的前后相邻的元素在多边形上也
是相邻的。3个以上的二分量List(一个二分量List为一个顶点)组成的List。
@return 若在多边形之内或者在多边形的边界上，返回True，否则返回False
'''
def is_in_2d_polygon(point, vertices):
    px = point[0]
    py = point[1]
    angle_sum = 0
 
    size = len(vertices)
    if size < 3:
        raise ValueError("len of vertices < 3")
    j = size - 1
    for i in range(0, size):
        sx = vertices[i][0]
        sy = vertices[i][1]
        tx = vertices[j][0]
        ty = vertices[j][1]
 
        # 通过判断点到通过两点的直线的距离是否为0来判断点是否在边上
        # y = kx + b, -y + kx + b = 0
        k = (sy - ty) / (sx - tx + 0.000000000001)  # 避免除0
        b = sy - k * sx
        dis = math.fabs(k * px - 1 * py + b) / math.sqrt(k * k + 1)
        if dis < 0.000001:  # 该点在直线上
            if sx <= px <= tx or tx <= px <= sx:  # 该点在边的两个定点之间，说明顶点在边上
                return True
 
        # 计算夹角
        angle = math.atan2(sy - py, sx - px) - math.atan2(ty - py, tx - px)
        # angle需要在-π到π之内
        if angle >= math.pi:
            angle = angle - math.pi * 2
        elif angle <= -math.pi:
            angle = angle + math.pi * 2
 
        # 累积
        angle_sum += angle
        j = i
 
    # 计算夹角和于2*pi之差，若小于一个非常小的数，就认为相等
    return math.fabs(angle_sum - math.pi * 2) < 0.00000000001


if __name__ == '__main__':

    # 爬取图片
    start = time()
    BingImagesSpider('人行街道', 2, 'images_spider').run()
    print(time() - start)


    get = GetCaptcha()
    get.get_number_and_letter('character/number_and_letter',num=5,num_img=2)
    get.get_pure_letter('character/pure_letter',num=5,num_img=2)
    get.get_pure_number('character/pure_number',num=5,num_img=2)

    get_number_operations('character/number_operations',num_img=2)

    get_behavior_drag('behavior/behavior_drag/captcha',num_captcha=2)

    get_behavior_rotate('behavior/behavior_rotate/background.png', 'behavior/behavior_rotate/captcha', num_captcha=2)
    
    get_behavior_object_recognition('behavior/behavior_object_recognition/test.png',
                                    [[250,240],[120,360],[490,360],[360,240]], # zebra crossing
                                    'behavior/behavior_object_recognition/captcha')

    
    
