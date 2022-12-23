import os
from time import time
from getcap.get_captcha import GetCaptcha, BingImagesSpider


if __name__ == '__main__':
    # 创建文件夹
    save_path_dir = 'datasets'
    if not os.path.exists(save_path_dir):
        os.makedirs(save_path_dir)

    #----------爬取图片测试--------------------#
    start = time()
    path1 = os.path.join(save_path_dir,'images_spider')
    if not os.path.exists(path1):
        os.makedirs(path1)
    BingImagesSpider('人行街道', 5, path1).run()
    print(time() - start)

    get = GetCaptcha()
    #---------字母数字组合验证码生成测试---------#
    path2 = os.path.join(save_path_dir,'captcha_nal')
    if not os.path.exists(path2):
        os.makedirs(path2)
    get.get_number_and_letter(path2,num=5,num_img=5)

    #---------纯字母验证码生成测试-------------#
    get.get_pure_letter(path2,num=5,num_img=5)

    #---------纯数字验证码生成测试---------#
    get.get_pure_number(path2,num=5,num_img=5)

    #---------数字运算验证码生成测试---------#
    path3 = os.path.join(save_path_dir,'captcha_nop')
    if not os.path.exists(path3):
        os.makedirs(path3)
    get.get_number_operations(path3,num_img=5)

    #---------滑块拖拽验证码生成测试---------#
    path4 = os.path.join(save_path_dir,'captcha_bd')
    if not os.path.exists(path4):
        os.makedirs(path4)
    get.get_behavior_drag(path4,num_captcha=5)

    #---------图片旋转验证码生成测试---------#
    path5 = os.path.join(save_path_dir,'captcha_br')
    if not os.path.exists(path5):
        os.makedirs(path5)
    get.get_behavior_rotate(path5, num_captcha=5)
    
    #---------物体识别验证码生成测试---------#
    path6 = os.path.join(save_path_dir,'captcha_bor')
    if not os.path.exists(path6):
        os.makedirs(path6)
    get.get_behavior_object_recognition(path6,'getcap/data/background.png',
                                       [[250,240],[120,360],[490,360],[360,240]])
