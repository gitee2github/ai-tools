import os
import torch
import math
import random
import argparse
import time
from captcha.image import ImageCaptcha
from torch import nn
from torch.utils.data import DataLoader
from dataloader import DLoader
from deploy_server.model.vgg import vgg
from deploy_server.model.resnet import resnet
from tqdm import tqdm


def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']

def get_train_dataset(data_path, cap_array, num_list=[4,5,6], num_per = 10000):
    max_num = max(num_list)
    image = ImageCaptcha(width=160,height=80)
    for num in num_list:
        for i in range(num_per):
            image_val  = "".join(random.sample(cap_array, num))
            image_name = os.path.join(data_path, "{}_{}.png".format(image_val + (max_num-num)*'#', int(time.time())))
            print(image_name)
            image.write(image_val,image_name)

def get_args_parser():
    parser = argparse.ArgumentParser('Set CAPTCHA recognition', add_help=False)
    parser.add_argument('--device', default='cuda', type=str, help='Device to use for training / testing. Set cuda for GPU device or cpu for CPU device')
    parser.add_argument('--model', default='ResNet18', type=str, help='Selection of identification model, options ResNet18/34/50/101 and VGG11/13/16/19.')
    parser.add_argument('--dataset_path', default='', type=str, help='If not specified, the training data set will be automatically generated.')
    parser.add_argument('--cap_array', default='123456789', type=str, help='The content of the verification code.')
    parser.add_argument('--batch_size', default=64, type=int)
    parser.add_argument('--train_lr', default=1e-3, type=float)
    parser.add_argument('--num_epoch', default=50, type=int)

    return parser

def main(args):
    captcha_array = args.cap_array + '#'
    if args.dataset_path == '':
        get_train_dataset("dataset/train", list(args.cap_array), num_list=[4,5,6], num_per=5000)
        train_datas   = DLoader("dataset/train",captcha_array)
    else:
        train_datas   = DLoader(args.dataset_path,captcha_array)
    train_dloader = DataLoader(train_datas,batch_size=args.batch_size,shuffle=True)
    out_size = 6 * captcha_array.__len__()
    if args.model[0] == 'R':
        model = resnet(model_name=args.model, num_classes=out_size)
    elif args.model[0] == 'V':
        model = vgg(model_name=args.model, num_classes=out_size)
    else:
        raise ValueError('could not find model : {}'.format(args.model))

    loss_fn = nn.MultiLabelSoftMarginLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.train_lr)
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma = 0.98)

    if args.device == 'cuda':
        model   = model.cuda()
        loss_fn = loss_fn.cuda()

    #-----------------------------------------------权重初始化-----------------------------------#
    for it in model.modules():
        if isinstance(it, nn.Conv2d):
            n = it.kernel_size[0] * it.kernel_size[1] * it.out_channels
            it.weight.data.normal_(0, math.sqrt(2. / n))
            if it.bias is not None: it.bias.data.zero_()

        elif isinstance(it, nn.BatchNorm2d):
            it.weight.data.fill_(0.1)
            it.bias.data.zero_()

        elif isinstance(it, nn.Linear):
            it.weight.data.normal_(0, 0.1)
            it.bias.data.zero_()
    #-----------------------------------------------训练-----------------------------------#
    num_train = train_datas.__len__() // args.batch_size
    model.train()
    
    for epoch in range(args.num_epoch):
        lr_item = get_lr(optimizer)
        print('epoch {} : Start training.'.format(epoch+1))
        pbar = tqdm(total=num_train, desc=f'Epoch {epoch+1}/{args.num_epoch}',postfix=dict,mininterval=0.3,ascii=False)#,ncols=150)
        avg_loss = 0
        for i,(imgs,tars) in enumerate(train_dloader):
            if i >= num_train: break

            imgs = imgs
            tars = tars
            if args.device == 'cuda':
                imgs = imgs.cuda()
                tars = tars.cuda()

            outputs = model(imgs)
            loss    = loss_fn(outputs, tars)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            avg_loss += loss.item()
            pbar.set_postfix(**{'loss'    : loss.item(),
                                'avg_loss': avg_loss/(i+1),
                                'lr'      : lr_item})
            pbar.update(1)

        pbar.close()
        torch.save(model.state_dict(),"model_weights.pth")
        lr_scheduler.step()
        print('epoch {} : End training.'.format(epoch + 1))

if __name__ == '__main__':
    parser = argparse.ArgumentParser('CAPTCHA recognition training script', parents=[get_args_parser()])
    args = parser.parse_args()
    main(args)
