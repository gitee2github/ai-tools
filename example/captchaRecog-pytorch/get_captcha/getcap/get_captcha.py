import os
import math
import random
import json
import requests
from lxml import etree
from time import time
from captcha.image import ImageCaptcha
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from multiprocessing.dummy import Pool

DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
DEFAULT_FONTS = os.path.join(DATA_DIR, 'DroidSansMono.ttf')
DEFAULT_BACK = os.path.join(DATA_DIR, 'background.png')
DEFAULT_SHAPE = os.path.join(DATA_DIR, 'shape.png')

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

    '''
    @description 生成数字与字母组合的4、5、6位验证码
    @param  save_path 生成验证码的保存路径，生成的验证码文件名为真值
    @param  num       验证码内的字符位数
    @param  num_img   生成验证码的数量
    @return 无
    '''
    def get_number_and_letter(self, save_path, num=4, num_img=1):
        self.get_base(save_path,list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"), num, num_img)

    '''
    @description 生成纯字母的4、5、6位验证码
    @param  save_path 生成验证码的保存路径，生成的验证码文件名为真值
    @param  num       验证码内的字符位数
    @param  num_img   生成验证码的数量
    @return 无
    '''
    def get_pure_letter(self, save_path, num=4, num_img=1):
        self.get_base(save_path,list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"), num, num_img)

    '''
    @description 生成纯数字的4、5、6位验证码
    @param  save_path 生成验证码的保存路径，生成的验证码文件名为真值
    @param  num       验证码内的字符位数
    @param  num_img   生成验证码的数量
    @return 无
    '''
    def get_pure_number(self, save_path, num=4, num_img=1):
        self.get_base(save_path,list("0123456789"), num, num_img)

    '''
    @description 生成数字计算（ +、-、x ）验证码
    @param  save_path 生成验证码的保存路径，生成的验证码文件名为真值
    @param  num_img   生成验证码的数量
    @return 无
    '''
    def get_number_operations(self, save_path, num_img = 1):
        font_file = DEFAULT_FONTS
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
                write_name = str(i)+'_'+str(a)+('X' if operation is 'x' else 'A')+str(b)+'.png'

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

    '''
    @description 生成滑块验证码
    @param  save_path  生成验证码的保存路径，
    @param  shape_path 滑块形状的图片路径，如果不指定则使用默认的形状
    @param  back_path  背景图片的路径，如果不指定则使用默认背景
    @param  num_img    生成验证码的数量
    @return 无
    '''
    def get_behavior_drag(self,save_path,shape_path=DEFAULT_SHAPE, back_path=DEFAULT_BACK, num_captcha=1):
        background_ = Image.open(back_path)
        shape_block = Image.open(shape_path).convert('RGBA')

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

    '''
    @description 生成旋转验证码
    @param  save_path      生成验证码的保存路径，文件名中包含旋转的角度（逆时针）
    @param  input_img_path 输入图片的路，如果不指定则使用默认
    @param  num_captcha    生成验证码的数量
    @return 无
    '''
    def get_behavior_rotate(self, save_path, input_img_path=DEFAULT_BACK ,num_captcha=1):
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


    '''
    @description 物体识别类的验证码生成（九宫格点选）
    @param  save_path      生成验证码的保存路径，文件名中包含旋转的角度（逆时针）
    @param  input_img_path 输入图片的路径，如果不指定则使用默认
    @param  object_pos     目标物体的位置（用来给出验证码的真值）list[[x1,y1],...]
    @return 无
    '''
    def get_behavior_object_recognition(self,save_path, input_img_path, object_pos):
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
                        if self._is_in_2d_polygon([ii,jj], object_pos): count += 1

                ans.append(count > 10)
                box_list.append(box)
                image_list = [image.crop(box) for box in box_list]
    
        #保存图片 
        index = 1
        for image in image_list: 
            image.save(os.path.join(save_path,name+'_'+str(index)+('_t' if ans[index-1] else '_f')+'.png'), 'PNG')
            index += 1

        print(os.path.split(input_img_path)[-1]+' : save completed!')

    def _is_in_2d_polygon(self, point, vertices):
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


class BingImagesSpider:
    thread_amount = 1000 # 线程池数量，线程池用于多IO请求，减少总的http请求时间
    per_page_images = 30 # 每页必应请求的图片数
    count = 0 # 图片计数
    success_count = 0
    # 忽略图片标签的一些字符
    ignore_chars = ['|', '.', '，', ',', '', '', '/', '@', ':', '：', ';', '；', '[', ']', '+']
    # 允许的图片类型
    image_types = ['bmp', 'jpg', 'png', 'tif', 'gif', 'pcx', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'ai', 'raw', 'WMF', 'webp']
    # 请求头
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    # 必应图片 url
    bing_image_url_pattern = 'https://www.bing.com/images/async?q={}&first={}&count={}&mmasync=1'
 
    def __init__(self, keyword, amount, path='./'):
        # keyword: 需爬取的关键字
        # amount: 需爬取的数量
        # path: 图片存放路径
        self.keyword = keyword
        self.amount = amount
        self.path = path
        self.thread_pool = Pool(self.thread_amount)
 
    def __del__(self):
        self.thread_pool.close()
        self.thread_pool.join()
 
    # 作用：从必应请求图片
    def request_homepage(self, url):
        # url: 必应图片页的 url
        return requests.get(url, headers=self.headers)
 
    # 作用：解析必应网页，得到所有图片的信息，封装到列表中返回
    # 每个图片的信息以字典对象存储，字典的键包括 image_title, image_type, image_md5, image_url
    def parse_homepage_response(self, response):
        # response: 必应网站的响应
        # 获取各图片信息所在的json格式字符串 m
        tree = etree.HTML(response.text)
        m_list = tree.xpath('//*[@class="imgpt"]/a/@m')
 
        # 对每个图片分别处理
        info_list = []
        for m in m_list:
            dic = json.loads(m)
 
            # 去除一些文件名中不允许的字符
            image_title = dic['t']
            for char in self.ignore_chars:
                image_title = image_title.replace(char, ' ')
            image_title = image_title.strip()
 
            # 有些图片的信息中不包含图片格式，该情况将图片设置为 jpg 格式
            image_type = dic['murl'].split('.')[-1]
            if image_type not in self.image_types:
                image_type = 'jpg'
 
            # 将每个图片的信息存为字典格式
            info = dict()
            info['image_title'] = image_title
            info['image_type'] = image_type
            info['image_md5'] = dic['md5']
            info['image_url'] = dic['murl']
 
            info_list.append(info)
        return info_list
 
    # 请求具体图片，保存到初始化时指定的路径
    def request_and_save_image(self, info):
        # info: 每个图片的信息,以字典对象存储。字典的键包括 image_title, image_type, image_md5, image_url
        try:
            # 请求图片
            response = requests.get(info['image_url'], headers=self.headers, timeout=1.5)
            filename = '{}_{}.{}'.format(self.count+1, self.keyword, info['image_type'])
            filepath = os.path.join(self.path, filename)
            # 保存图片
            with open(filepath, 'wb') as fp:
                fp.write(response.content)
            # 打印日志
            self.count += 1
            self.success_count += 1
            print('{}: saving {} done.'.format(self.count, filepath))
 
        except requests.exceptions.RequestException as e:
            self.count += 1
            print('{}: saving {}failed. url: {}'.format(self.count, filepath, info['image_url']))
            print('\t tip:', e)
 
    # 作用：图片信息的列表去重，去除重复的图片信息
    def deduplication(self, info_list):
        result = []
 
        # 用图片的 md5 做为唯一标识符
        md5_set = set()
        for info in info_list:
            if info['image_md5'] not in md5_set:
                result.append(info)
                md5_set.add(info['image_md5'])
        return result
 
    # 作用：运行爬虫，爬取图片
    def run(self):
        # 创建用于保存图片的目录
        if not os.path.exists(self.path):
            os.mkdir(self.path)
 
        # 根据关键词和需要的图片数量，生成将爬取的必应图片网页列表
        homepage_urls = []
        for i in range(int(self.amount/self.per_page_images * 1.5) + 1): # 由于有些图片会重复，故先请求1.5倍图片，豁免
            url = self.bing_image_url_pattern.format(self.keyword, i*self.per_page_images, self.per_page_images)
            homepage_urls.append(url)
        print('homepage_urls len {}'.format(len(homepage_urls)))
 
        # 通过线程池请求所有必应图片网页
        homepage_responses = self.thread_pool.map(self.request_homepage, homepage_urls)
 
        # 从必应网页解析所有图片的信息，每个图片包括 image_title, image_type, image_md5, image_url 等信息。
        info_list = []
        for response in homepage_responses:
            result = self.parse_homepage_response(response)
            info_list += result
        print('info amount before deduplication', len(info_list))
 
        # 删除重复的图片，避免重复下载
        info_list = self.deduplication(info_list)
        print('info amount after deduplication', len(info_list))
        info_list = info_list[ : self.amount]
        print('info amount after split', len(info_list))
 
        # 下载所有图片，并保存
        self.thread_pool.map(self.request_and_save_image, info_list)
        print('all done. {} successfully downloaded, {} failed.'.format(self.success_count, self.count - self.success_count))


    
    
