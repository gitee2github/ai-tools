import torch
import torch.nn.functional as F

def text2vec(text,captcha_array,captcha_size=6):
    vectors = torch.zeros((captcha_size,captcha_array.__len__()))
    for i in range(len(text)):
        vectors[i,captcha_array.index(text[i])] = 1

    return vectors

def vectotext(vec,captcha_array):
    vec = torch.argmax(vec,dim=1)
    text_label = ""
    for v in vec:
        text_label += captcha_array[v]
    return  text_label