import requests
import argparse
import random
import os
from captcha.image import ImageCaptcha

BASE_DIR = '/root/ai-tools/recogcap/resources/test_images'
ARGS = {}

def get_args_parser():
    parser = argparse.ArgumentParser('Set client', add_help=False)
    parser.add_argument('--url', default='http://127.0.0.1:5000', type=str)
    parser.add_argument('--test', action='store_true',default=False,help='Whether to automatically generate captcha for testing.')

    return parser

def get_test_dataset(data_path, cap_array, num_list=[4,5,6]):
    image = ImageCaptcha(width=160,height=80)
    num = random.sample(num_list, 1)[0]

    image_val  = "".join(random.sample(cap_array, num))
    image_name = os.path.join(data_path, "test.png".format(image_val))
    image.write(image_val,image_name)
    return image_name

# 主函数
def main():
    parser = argparse.ArgumentParser('recogcap client script', parents=[get_args_parser()])
    global ARGS
    ARGS = parser.parse_args()
    
    if ARGS.test:
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
        imageFilePath = get_test_dataset(BASE_DIR, '0123456789', num_list=[4,5,6])
        print('Test pictures have been randomly generated and saved in : {}'.format(imageFilePath))
    else:
        while True:
            input_content = input('Enter picture path :')
            if not os.path.exists(input_content.strip()):
                print('The input picture path is incorrect, please re-enter!')
            else:
                imageFilePath = input_content.strip()
                break

    imageFileName = os.path.split(imageFilePath)[1]
    file_dict = {
        'file':(imageFileName,
            open(imageFilePath,'rb'),
            'image/png')}
    result = requests.post(ARGS.url, files=file_dict)
    predict_result = result.text
    print('Picture : {} , the result is : {}'.format(imageFilePath, predict_result.replace('#','')))

if __name__ == "__main__":
    main()
    
