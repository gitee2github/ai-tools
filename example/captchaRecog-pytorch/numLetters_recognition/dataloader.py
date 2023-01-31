import os
from PIL import Image
import numpy as np
import torch
from torch.utils.data import Dataset
import util.one_hot as one_hot

class DLoader(Dataset):
    def __init__(self,root_dir,captcha_array,captcha_size=6,test=False):
        super(DLoader, self).__init__()
        self.list_image_path = []
        for image_name in os.listdir(root_dir):
            if image_name.split('.')[-1] == 'png': 
                self.list_image_path.append(os.path.join(root_dir,image_name))
        self.test = test
        self.captcha_array = captcha_array
        self.captcha_size = captcha_size

    def __getitem__(self, index):
        image_path = self.list_image_path[index]
        img_       = Image.open(image_path)
        orw,orh    = img_.size
        image_name = os.path.split(image_path)[-1]
        img_       = img_.convert('L')
        img_       = np.array(img_)
        black_lab  = np.ones((max(orh,orw//2),orw))*img_[0,0] # 2:1的宽高比
        black_lab[:img_.shape[0],:img_.shape[1]] = img_
        img_       = Image.fromarray(black_lab)
        img_       = img_.resize((160,80))
        img_tesor  = torch.tensor(np.array(img_, np.float32) / 255.0).unsqueeze(0)

        lable_test = image_name.split("_")[0]
        img_lable  = one_hot.text2vec(lable_test,self.captcha_array,self.captcha_size)
        img_lable  = img_lable.view(1,-1)[0]
        if self.test:
            return img_tesor,lable_test
        else:
            return img_tesor,img_lable

    def __len__(self):
        return self.list_image_path.__len__()


