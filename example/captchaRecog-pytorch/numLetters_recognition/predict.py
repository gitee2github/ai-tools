import os
import argparse
import torch
import random
import time
import dataloader
import numpy as np
from PIL import Image
from torch.utils.data import DataLoader
import util.one_hot as one_hot
from captcha.image import ImageCaptcha
from deploy_server.model.vgg import vgg
from deploy_server.model.resnet import resnet

def get_test_dataset(data_path, cap_array='123456789', num_list=[4,5,6], num_per=500):
    image = ImageCaptcha(width=160,height=80)
    for num in num_list:
        for i in range(num_per):
            image_val  = "".join(random.sample(cap_array, num))
            image_name = os.path.join(data_path, "{}_{}.png".format(image_val, int(time.time())))
            print(image_name)
            image.write(image_val,image_name)

def get_args_parser():
    parser = argparse.ArgumentParser('Set CAPTCHA recognition', add_help=False)
    parser.add_argument('--device', default='cpu', type=str, help='Device to use for training / testing. Set cuda for GPU device or cpu for CPU device')
    parser.add_argument('--model', default='ResNet18', type=str, help='Selection of identification model, options ResNet18/34/50/101 and VGG11/13/16/19.')
    parser.add_argument('--model_path', default='', type=str, help='Path of model file.')
    parser.add_argument('--dataset_path', default='', type=str, help='If not specified, the testing data set will be automatically generated.')
    parser.add_argument('--cap_array', default='0123456789', type=str, help='The content of the verification code.')

    return parser

def pred_pics(args):
    captcha_array = args.cap_array + '#'
    out_size = 6 * captcha_array.__len__()
    print('load model.')
    device = torch.device(args.device)
    state_dict = torch.load(args.model_path, map_location=device)
    
    if args.model[0] == 'R':
        m = resnet(model_name=args.model, num_classes=out_size)
    elif args.model[0] == 'V':
        m = vgg(model_name=args.model, num_classes=out_size)
    else:
        raise ValueError('could not find model : {}'.format(args.model))
    if args.device == 'cuda' : m = m.cuda()
    m.load_state_dict(state_dict)
    print('load success.')
    
    if args.dataset_path == '':
        get_test_dataset('dataset/test', cap_array='123456789', num_list=[4,5,6], num_per=500)
        test_data = dataloader.DLoader('dataset/test',captcha_array,test=True)
    else:
        test_data = dataloader.DLoader(args.dataset_path,captcha_array,test=True)
    test_loader = DataLoader(test_data, batch_size=1, shuffle=False)
    test_length = test_data.__len__()
    correct = 0
    m.eval()
    for i, (imgs, lable) in enumerate(test_loader):
        imgs = imgs
        lable_t = lable[0]
        if args.device == 'cuda' : imgs = imgs.cuda()

        predict_outputs = m(imgs)
        predict_outputs = predict_outputs.view(-1, captcha_array.__len__())
        predict_labels  = one_hot.vectotext(predict_outputs,captcha_array)

        if predict_labels.replace('#', '') == lable_t.replace('#', ''):
            correct += 1
            print("预测正确：正确值:{},预测值:{}".format(lable_t, predict_labels))
        else:
            print("预测失败:正确值:{},预测值:{}".format(lable_t, predict_labels))

    print("正确率{}".format(correct / test_length * 100))

def pred_pic(args):
    captcha_array = args.cap_array + '#'
    out_size = 6 * captcha_array.__len__()
    print('load model.')
    device = torch.device(args.device)
    state_dict = torch.load(args.model_path, map_location=device)
    
    if args.model[0] == 'R':
        model = resnet(model_name=args.model, num_classes=out_size)
    elif args.model[0] == 'V':
        model = vgg(model_name=args.model, num_classes=out_size)
    else:
        raise ValueError('could not find model : {}'.format(args.model))
    if args.device == 'cuda' : model = model.cuda()
    model.load_state_dict(state_dict)
    print('load success.')

    while True:
        img_name = input('Input image filename : ')
        try:
            img_or    = Image.open(img_name)
            orw,orh   = img_or.size
            img       = img_or.convert('L')
            img       = np.array(img)
            black_lab = np.ones((max(orh,orw//2),orw))*img[0,0] # 2:1的宽高比
            black_lab[:img.shape[0],:img.shape[1]] = img
            img       = Image.fromarray(black_lab)
            img       = img.resize((160,80))
            img       = torch.tensor(np.array(img, np.float32) / 255.0)

            if args.device == 'cuda' : img = img.cuda()

        except:
            print('Open Error! Try again!')
            continue
        else:
            model.eval()
            with torch.no_grad():
                img = torch.reshape(img,(-1,1,80,160))
                outputs = model(img)
                outputs = outputs.view(-1,len(captcha_array))
                lable   = one_hot.vectotext(outputs,captcha_array)
                print('--------------------------')
                print('result : ',lable)
                print('--------------------------')
                img_or.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser('CAPTCHA recognition training script', parents=[get_args_parser()])
    args = parser.parse_args()

    # 测试集的命名规则为 正确答案_任意内容.png r"..\get_captcha\character\pure_number"
    pred_pics(args)

    # 单张测试 测试集的命名规则为 正确答案_任意内容.png
    # pred_pic(args)

