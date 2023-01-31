# -*- coding: utf-8 -*-
import time
import argparse
import os
import torch
from PIL import Image
import numpy as np
from flask import request, Flask
from .model.vgg import vgg
from .model.resnet import resnet

recogcap = Flask(__name__)

BASE_DIR = '/root/ai-tools/recogcap/'
LOG_DIR = os.path.join(BASE_DIR,'log')
ARGS = {}

def get_args_parser():
    parser = argparse.ArgumentParser('Set server', add_help=False)
    parser.add_argument('--host', default="127.0.0.1", type=str)
    parser.add_argument('--port', default=5000, type=int)
    parser.add_argument('--model', default='ResNet18', type=str, help='Selection of identification model, options ResNet18/34/50/101 and VGG11/13/16/19.')
    parser.add_argument('--model_path', default='', type=str, help='Path of model file.')
    parser.add_argument('--cap_array', default='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', type=str, help='The content of the verification code.')

    return parser

def vectotext(vec,captcha_array):
    vec = torch.argmax(vec,dim=1)
    text_label = ""
    for v in vec:
        text_label += captcha_array[v]
    return  text_label

def get_image(imageFilePath):
    img_or    = Image.open(imageFilePath)
    orw,orh   = img_or.size
    img       = img_or.convert('L')
    img       = np.array(img)
    black_lab = np.ones((max(orh,orw//2),orw))*img[0,0] # 2:1的宽高比
    black_lab[:img.shape[0],:img.shape[1]] = img
    img       = Image.fromarray(black_lab)
    img       = img.resize((160,80))
    img       = torch.tensor(np.array(img, np.float32) / 255.0)
    return img

def predict_image(imageFilePath, captcha_array):
    captcha_array = captcha_array + '#'
    out_size = 6 * captcha_array.__len__()
    dev = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if ARGS.model_path != '':
        state_dict = torch.load(ARGS.model_path, map_location=dev)
    else:
        state_dict = torch.load(os.path.join(BASE_DIR,'resources/weights/model_weights.pth'),map_location=dev)
    if ARGS.model[0] == 'R':
        model = resnet(model_name=ARGS.model, num_classes=out_size)
    elif ARGS.model[0] == 'V':
        model = vgg(model_name=ARGS.model, num_classes=out_size)
    else:
        raise ValueError('could not find model : {}'.format(ARGS.model))

    model.load_state_dict(state_dict)
    model.eval()
    img = get_image(imageFilePath)
    if torch.cuda.is_available():
        img = img.cuda()
        model = model.cuda()
    with torch.no_grad():
        img = torch.reshape(img,(-1,1,80,160))
        outputs = model(img)
        outputs = outputs.view(-1,len(captcha_array))
        lable   = vectotext(outputs,captcha_array)

        return lable

@recogcap.route("/", methods=['POST'])
def result():
    log_path = os.path.join(LOG_DIR,'recogcap-s.log')
    log = open(log_path, 'a')

    log.write('[{}] #------------------------------#\n'.format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    log.write('[{}] Runing at http://{}:{}.\n'.format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        ARGS.host,str(ARGS.port)))

    startTime = time.time()
    received_file = request.files['file']
    image_filename = received_file.filename
    if received_file:
        received_dirPath = os.path.join(BASE_DIR,'resources/received_images')
        if not os.path.isdir(received_dirPath):
            os.makedirs(received_dirPath)
        image_file_path = os.path.join(received_dirPath, image_filename)
        received_file.save(image_file_path)

        log.write('[{}] Picture files saved in : {}.\n'.format(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            image_file_path))

        print('Save picture files to this path : %s.' % image_file_path)
        print('Receive and save pictures, taking %.2f seconds in total.' % (time.time() - startTime))

        log.write('[{}] Start predicting.\n'.format(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            image_file_path))

        result = predict_image(image_file_path,ARGS.cap_array)

        log.write('[{}] Prediction complete. Total time : {}. Result : {}.\n'.format(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            (time.time() - startTime),result))
        log.write('[{}] #------------------------------#\n'.format(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        

        print('The prediction of the received picture is completed, which takes %.2f seconds in total.' % (time.time() - startTime))
        print("Result : ",result)
        return result
    else:
        return 'Failed'


# 主函数
def main():
    parser = argparse.ArgumentParser('recogcap server script', parents=[get_args_parser()])
    global ARGS
    ARGS = parser.parse_args()
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    recogcap.run(host=ARGS.host, port=ARGS.port)

if __name__ == "__main__":
    main()

