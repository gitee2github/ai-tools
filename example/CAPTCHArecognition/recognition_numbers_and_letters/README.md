#### 介绍
本项目旨在基于openEuler实现验证码识别功能，做为openEuler的基本AI能力级。目前本项目利用数字字母以及占位符的one-hot编码，可以实现4、5、6（可根据需求自己设置）位数字字母组合的验证码识别功能。训练和验证数据集来自python的captcha库的生成以及一部分网络数据集。
#### 环境
openEuler-22.03-LTS + pytorch-1.6.0（`https://gitee.com/src-openeuler/pytorch.git`）详见requirements.txt

#### 训练
**参数说明：**
<table>
  <thead>
    <tr style="text-align: center;">
      <th></th>
      <th>参数名称</th>
      <th>类型</th>
      <th>默认值</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>--device</td>
      <td>str</td>
      <td>cuda</td>
      <td>训练时所使用的设备，默认是使用GPU进行训练，如果需要使用CPU训练需要改成'cpu'</td>
    </tr>
    <tr>
      <th>1</th>
      <td>--model</td>
      <td>str</td>
      <td>ResNet18</td>
      <td>识别时所使用的主干网络选择。本项目测试的综合性能'ResNet18'最佳，如果使用者想尝试其他网络，本项目提供了参数接口，可根据不同的需求选择ResNet18/34/50/101和VGG11/13/16/19</td>
    </tr>
    <tr>
      <th>2</th>
      <td>--dataset_path</td>
      <td>str</td>
      <td>(空)</td>
      <td>如果此项为空字符串，即未指定训练集路径，本项目将根据--cap_array的参数，使用captcha库自动生成训练数据集，并将数据集放到项目目录下的dataset/train中</td>
    </tr>
	<tr>
      <th>3</th>
      <td>--cap_array</td>
      <td>str</td>
      <td>0123456789</td>
      <td>此参数用于指定验证码的内容，如果要训练4、5、6位的纯数字验证码的识别则使用默认参数即可</td>
    </tr>
	<tr>
      <th>4</th>
      <td>--batch_size</td>
      <td>int</td>
      <td>64</td>
      <td>数据集的批大小，即单次传递给程序用以训练的数据(样本)个数</td>
    </tr>
	<tr>
      <th>5</th>
      <td>--train_lr</td>
      <td>float</td>
      <td>1e-3</td>
      <td>学习率</td>
    </tr>
	<tr>
      <th>6</th>
      <td>--num_epoch</td>
      <td>int</td>
      <td>50</td>
      <td>训练轮数</td>
    </tr>
  </tbody>
</table>

**训练示例：**`python train.py --device cpu --cap_array 0123456789abcdefghijklmnopqrstuvwxyz --batch_size 16`

#### 测试
**参数说明：**
<table>
  <thead>
    <tr style="text-align: center;">
      <th></th>
      <th>参数名称</th>
      <th>类型</th>
      <th>默认值</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>--device</td>
      <td>str</td>
      <td>cuda</td>
      <td>训练时所使用的设备，默认是使用GPU进行训练，如果需要使用CPU训练需要改成'cpu'</td>
    </tr>
    <tr>
      <th>1</th>
      <td>--model_path</td>
      <td>str</td>
      <td>(空)</td>
      <td>.pth模型文件的路径</td>
    </tr>
    <tr>
      <th>2</th>
      <td>--dataset_path</td>
      <td>str</td>
      <td>(空)</td>
      <td>如果此项为空字符串，即未指定训练集路径，本项目将根据--cap_array的参数，使用captcha库自动生成测试数据集（4、5、6位三种验证码），并将数据集放到项目目录下的dataset/test中</td>
    </tr>
	<tr>
      <th>3</th>
      <td>--cap_array</td>
      <td>str</td>
      <td>0123456789</td>
      <td>此参数用于指定验证码的内容，如果要验证的--model_path的模型文件是4、5、6位的纯数字验证码的识别则使用默认参数即可</td>
    </tr>
  </tbody>
</table>

**测试示例（本示例为批量测试，本项目内含有单张测试的接口）：**
<table>
  <thead>
    <tr style="text-align: center;">
      <th></th>
      <th>模型文件</th>
      <th>训练数据集</th>
      <th>准确率</th>
	  <th>cap_array</th>
      <th>下载地址</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>model_weights_r18_6</td>
      <td>captcha库自动生成的</td>
      <td>97%</td>
	  <td>0123456789abcdefghijklmnopqrstuvwxyz</td>
      <td>链接：https://pan.baidu.com/s/1utCCN9kAYitMzmm-NYultA，提取码：yn50</td>
    </tr>

  </tbody>
</table>

示例：`python predict.py --device cpu --model_path model_weights_r18_6 --cap_array 0123456789abcdefghijklmnopqrstuvwxyz`