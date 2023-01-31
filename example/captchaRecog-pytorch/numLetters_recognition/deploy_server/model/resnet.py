import torch
import torch.nn as nn

# 定义18层和34层网络所用的残差结构
class BasicBlock(nn.Module):
    # 对应残差分支中主分支采用的卷积核个数有无发生变化，无变化设为1（即每一个残差结构主分支的第二层卷积层卷积核个数是第一层卷积层卷积核个数的1倍）
    expansion = 1
 
    # 输入特征矩阵深度、输出特征矩阵深度（主分支卷积核个数）、步长默认取1、下采样参数默认为None（对应虚线残差结构）
    def __init__(self, in_channel, out_channel, stride=1, downsample=None, **kwargs):
        super(BasicBlock, self).__init__()
        # 每一个残差结构中主分支第一个卷积层，注意步长是要根据是否需要改变channel而取1或取2的，不使用偏置（BN处理）
        self.conv1 = nn.Conv2d(in_channels=in_channel, out_channels=out_channel,
                               kernel_size=3, stride=stride, padding=1, bias=False)
        # BN标准化处理，输入特征矩阵为conv1的out_channel
        self.bn1 = nn.BatchNorm2d(out_channel)
        # 激活函数
        self.relu = nn.ReLU()
        # 每一个残差结构中主分支第二个卷积层，输入特征矩阵为bn1的out_channel，该卷积层步长均为1，不使用偏置
        self.conv2 = nn.Conv2d(in_channels=out_channel, out_channels=out_channel,
                               kernel_size=3, stride=1, padding=1, bias=False)
        # BN标准化处理，输入特征矩阵为conv2的out_channel
        self.bn2 = nn.BatchNorm2d(out_channel)
        # 下采样方法，即侧分支为虚线
        self.downsample = downsample
 
    # 正向传播过程
    def forward(self, x):
        # 将输入特征矩阵赋值给identity（副分支的输出值）
        identity = x
        # 如果需要下采样方法，将输入特征矩阵经过下采样函数再赋值给identity
        if self.downsample is not None:
            identity = self.downsample(x)
 
        # 主分支的传播过程
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
 
        out = self.conv2(out)
        out = self.bn2(out)
 
        # 将主分支和副分支的输出相加再经过激活函数
        out += identity
        out = self.relu(out)
 
        return out

# 定义50层、101层和152层网络所用的残差结构
class Bottleneck(nn.Module):
    # 每一个残差结构主分支的第三层卷积层卷积核个数是第一层或第二层卷积层卷积核个数的4倍）
    expansion = 4
 
    # 输入特征矩阵深度、输出特征矩阵深度（和18层和34层网络残差结构的主分支卷积核个数相同）、步长默认取1、下采样参数默认为None（对应虚线残差结构）、最后两个参数和ResNeXt网络的搭建有关
    def __init__(self, in_channel, out_channel, stride=1, downsample=None,
                 groups=1, width_per_group=64):
        super(Bottleneck, self).__init__()
 
        # ResNeXt网络的搭建
        width = int(out_channel * (width_per_group / 64.)) * groups
 
        # 每一个残差结构中主分支第一个卷积层，卷积核为1*1，不使用偏置
        self.conv1 = nn.Conv2d(in_channels=in_channel, out_channels=width,
                               kernel_size=1, stride=1, bias=False)  # squeeze channels
        # BN标准化处理，输入特征矩阵为conv1的width
        self.bn1 = nn.BatchNorm2d(width)
        # -----------------------------------------
        # 每一个残差结构中主分支第二个卷积层，卷积核为3*3
        self.conv2 = nn.Conv2d(in_channels=width, out_channels=width, groups=groups,
                               kernel_size=3, stride=stride, bias=False, padding=1)
        # BN标准化处理，输入特征矩阵为conv2的width
        self.bn2 = nn.BatchNorm2d(width)
        # -----------------------------------------
        # 每一个残差结构中主分支第二个卷积层，卷积核为1*1，输出特征矩阵为4倍的第一层或第二层卷积的卷积核个数
        self.conv3 = nn.Conv2d(in_channels=width, out_channels=out_channel*self.expansion,
                               kernel_size=1, stride=1, bias=False)  # unsqueeze channels
        # BN标准化处理，输入特征矩阵为conv3的out_channel*self.expansion
        self.bn3 = nn.BatchNorm2d(out_channel*self.expansion)
        # 激活函数
        self.relu = nn.ReLU(inplace=True)
        # 下采样方法，即侧分支为虚线
        self.downsample = downsample
 
    # 正向传播过程
    def forward(self, x):
        identity = x
        if self.downsample is not None:
            identity = self.downsample(x)
 
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
 
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)
 
        out = self.conv3(out)
        out = self.bn3(out)
 
        out += identity
        out = self.relu(out)
 
        return out

# 定义ResNet网络结构
class ResNet(nn.Module):
 
    # 对应哪一种残差结构、残差结构数目（是一个列表值，如ResNet-34为[3, 4, 6, 3]）、分类个数、方便在ResNet网络基础上搭建更加复杂的网络
    def __init__(self,
                 block,
                 blocks_num,
                 num_classes=1000,
                 include_top=True,
                 groups=1,
                 width_per_group=64):
        super(ResNet, self).__init__()
        self.include_top = include_top
        # 输入矩阵深度，对应3*3maxpool后所得到的特征矩阵深度，不论多少层的ResNet网络均为64
        self.in_channel = 64
        
        # ResNeXt网络的搭建
        self.groups = groups
        self.width_per_group = width_per_group
        self.features = nn.Sequential(
            # 第一层卷积层，输入RGB图像深度为3，64个7*7的卷积核，为了让输出特征矩阵的H和W变为原来一半padding设置为3
            nn.Conv2d(1, self.in_channel, kernel_size=7, stride=2,
                      padding=3, bias=False),
            # BN层
            nn.BatchNorm2d(self.in_channel),
            # 激活函数
            nn.ReLU(inplace=True),
            # 最大池化下采样层，为了让输出特征矩阵的H和W变为原来一半padding设置为1
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            # conv2_x，通过_make_layer函数生成，注意该层输入的是maxpool输出的56*56的矩阵，因此不需要步长为2来减半，故步长默认为1
            self._make_layer(block, 64, blocks_num[0]),
            # conv3_x
            self._make_layer(block, 128, blocks_num[1], stride=2),
            # conv4_x
            self._make_layer(block, 256, blocks_num[2], stride=2),
            # conv5_x
            self._make_layer(block, 512, blocks_num[3], stride=2)
        )
        if self.include_top:
            # 平均池化下采样层
            self.avgpool = nn.AdaptiveAvgPool2d((1, 1))  # output size = (1, 1)
            # 全连接层，节点个数可能为512也可能为512*4
            self.fc = nn.Linear(512 * block.expansion, num_classes)
        # 对卷积层进行初始化操作
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
 
    # 生成conv2_x、conv3_x、conv4_x、conv5_x的函数
    # 选择哪种残差结构、主分支第一层卷积核个数、该层一共包含了多少个残差结构、步长默认为1
    def _make_layer(self, block, channel, block_num, stride=1):
        downsample = None
        # 步长不为1或者conv2、3、4、5_x的第一个卷积层卷积核个数不等于最后一层卷积核个数（即expansion是否为4）
        # 若为ResNet-18、34的虚线残差结构，前一项为True；若为ResNet-50、101、152的虚线残差结构，前后均为为True
        # 故前一项是为了保证ResNet-18、34的conv3、4、5_x的判断能够通过
        if stride != 1 or self.in_channel != channel * block.expansion:
            # 生成副分支，输入为输入convx_x的特征矩阵，输出为1倍或4倍，步长为1或2
            downsample = nn.Sequential(
                nn.Conv2d(self.in_channel, channel * block.expansion, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(channel * block.expansion))
 
        # 定义一个空列表，用来装convx_x的网络结构
        layers = []
        # 首先要把第一个残差结构加进去，因为第一个残差结构涉及到虚线残差结构
        layers.append(block(self.in_channel,
                            channel,
                            downsample=downsample,
                            stride=stride,
                            groups=self.groups,
                            width_per_group=self.width_per_group))
        # 经过convx_x后输入conv(x+1)_x的channel变为1倍或4倍
        self.in_channel = channel * block.expansion
        # 把后面的残差结构加上，不涉及虚线残差结构
        for _ in range(1, block_num):
            layers.append(block(self.in_channel,
                                channel,
                                groups=self.groups,
                                width_per_group=self.width_per_group))
 
        # 将层结构组合在一起并且返回
        return nn.Sequential(*layers)
    # 整个网络的正向传播过程
    def forward(self, x):
        x = self.features(x)
        
        if self.include_top:
            x = self.avgpool(x)
            # 展平
            x = torch.flatten(x, 1)
            x = self.fc(x)
 
        return x

def resnet(model_name="ResNet18",num_classes=1000, include_top=True):
    if model_name == "ResNet18":
        return ResNet(BasicBlock, [2, 2, 2, 2], num_classes=num_classes, include_top=include_top)
    elif model_name == "ResNet34":
        return ResNet(BasicBlock, [3, 4, 6, 3], num_classes=num_classes, include_top=include_top)
    elif model_name == "ResNet50":
        return ResNet(Bottleneck, [3, 4, 6, 3], num_classes=num_classes, include_top=include_top)
    elif model_name == "ResNet101":
        return ResNet(Bottleneck, [3, 4, 23, 3], num_classes=num_classes, include_top=include_top)
    elif model_name == "ResNet152":
        return ResNet(Bottleneck, [3, 8, 36, 3], num_classes=num_classes, include_top=include_top)
    else:
        raise ValueError('could not find {}'.format(model_name))
