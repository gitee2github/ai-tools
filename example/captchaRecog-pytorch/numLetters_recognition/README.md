# recogcap
## 介绍
本项目旨在基于openEuler实现验证码识别功能，做为openEuler的基本AI能力级。目前本项目利用数字字母以及占位符的one-hot编码，可以实现4、5、6（可根据需求自己设置）位数字字母组合的验证码识别功能。训练和验证数据集来自python的captcha库的生成以及一部分网络数据集。
## 环境
openEuler-22.03-LTS + pytorch-1.6.0（`https://gitee.com/src-openeuler/pytorch.git`）详见requirements.txt
## 目录结构

	```text
	.
	├── dataloader.py
	├── dataset
	│   ├── test
	│   └── train
	├── deploy_client
	│   ├── __init__.py
	│   ├── recogcap_client.py
	│   └── rpm
	│       └── recogcap-c.spec
	├── deploy_server
	│   ├── __init__.py
	│   ├── model
	│   │   ├── __init__.py
	│   │   ├── resnet.py
	│   │   └── vgg.py
	│   ├── recogcap_server.py
	│   ├── resources
	│   │   └── weights
	│   ├── rpm
	│   │   └── recogcap-s.spec
	│   └── service
	│       ├── recogcap-s.conf
	│       ├── recogcap-s.service
	│       └── recogcap-s.sh
	├── dist
	│   ├── recogcap-c-1.0.0-1.noarch.rpm
	│   └── recogcap-s-1.0.0-1.noarch.rpm
	├── predict.py
	├── README.md
	├── requirements.txt
	├── setup-c.py
	├── setup-s.py
	├── train.py
	└── util
	    ├── one_hot.py
	    └── rename.py
	```

## 训练
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
	      <td>`--device`</td>
	      <td>str</td>
	      <td>`cuda`</td>
	      <td>训练时所使用的设备，默认是使用GPU进行训练，如果需要使用CPU训练需要改成`cpu`</td>
	    </tr>
	    <tr>
	      <th>1</th>
	      <td>`--model`</td>
	      <td>str</td>
	      <td>`ResNet18`</td>
	      <td>识别时所使用的主干网络选择。本项目测试的综合性能`'ResNet18'`最佳，如果使用者想尝试其他网络，本项目提供了参数接口，可根据不同的需求选择ResNet18/34/50/101和VGG11/13/16/19</td>
	    </tr>
	    <tr>
	      <th>2</th>
	      <td>`--dataset_path`</td>
	      <td>str</td>
	      <td>(空)</td>
	      <td>如果此项为空字符串，即未指定训练集路径，本项目将根据`--cap_array`的参数，使用captcha库自动生成训练数据集，并将数据集放到项目目录下的`dataset/train`中</td>
	    </tr>
		<tr>
	      <th>3</th>
	      <td>`--cap_array`</td>
	      <td>str</td>
	      <td>`0123456789`</td>
	      <td>此参数用于指定验证码的内容，如果要训练4、5、6位的纯数字验证码的识别则使用默认参数即可</td>
	    </tr>
		<tr>
	      <th>4</th>
	      <td>`--batch_size`</td>
	      <td>int</td>
	      <td>`64`</td>
	      <td>数据集的批大小，即单次传递给程序用以训练的数据(样本)个数</td>
	    </tr>
		<tr>
	      <th>5</th>
	      <td>`--train_lr`</td>
	      <td>float</td>
	      <td>`1e-3`</td>
	      <td>学习率</td>
	    </tr>
		<tr>
	      <th>6</th>
	      <td>`--num_epoch`</td>
	      <td>int</td>
	      <td>`50`</td>
	      <td>训练轮数</td>
	    </tr>
	  </tbody>
	</table>

**训练示例：**`python train.py --device cpu --cap_array 0123456789abcdefghijklmnopqrstuvwxyz --batch_size 16`

## 测试
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
	      <td>`--device`</td>
	      <td>str</td>
	      <td>`cuda`</td>
	      <td>训练时所使用的设备，默认是使用GPU进行训练，如果需要使用CPU训练需要改成'cpu'</td>
	    </tr>
	    <tr>
	      <th>1</th>
	      <td>`--model_path`</td>
	      <td>str</td>
	      <td>(空)</td>
	      <td>.pth模型文件的路径，必须使用该参数，否则将无法加载模型权重</td>
	    </tr>
	    <tr>
	      <th>2</th>
	      <td>`--dataset_pat`h</td>
	      <td>str</td>
	      <td>(空)</td>
	      <td>如果此项为空字符串，即未指定训练集路径，本项目将根据`--cap_array`的参数，使用captcha库自动生成测试数据集（4、5、6位三种验证码），并将数据集放到项目目录下的`dataset/test`中</td>
	    </tr>
		<tr>
	      <th>3</th>
	      <td>`--cap_array`</td>
	      <td>str</td>
	      <td>`0123456789`</td>
	      <td>此参数用于指定验证码的内容，如果要验证的`--model_path`的模型文件是4、5、6位的纯数字验证码的识别则使用默认参数即可</td>
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
	      <td>`model_weights.pth`</td>
	      <td>captcha库自动生成的</td>
	      <td>97%</td>
		  <td>`0123456789abcdefghijklmnopqrstuvwxyz`</td>
	      <td>链接：`https://pan.baidu.com/s/1c1sl4tGpEzXdWam1Xwe5BA` 提取码：`1k54`</td>
	    </tr>
	  </tbody>
	</table>
将下载好的模型文件`model_weights.pth`放到`ai-tools/example/captchaRecog-pytorch/numLetters_recognition/deploy_server/resources/weights`

示例：`python predict.py --device cpu --model_path deploy_server/resources/weights/model_weights.pth --cap_array 0123456789abcdefghijklmnopqrstuvwxyz`

## 快速开始
#### 环境
1. openEuler-22.03-LTS
2. python3 
#### recogcap-s 验证码识别服务端部署

1. 基于源码编译、安装、运行
	- 下载源码
   
     ```
     git clone https://gitee.com/openeuler/ai-tools.git
     ```

	 ```
     cd ai-tools/example/captchaRecog-pytorch/numLetters_recognition
     ```
	- 下载模型文件

	链接：`https://pan.baidu.com/s/1c1sl4tGpEzXdWam1Xwe5BA` 提取码：`1k54`

	将模型文件`model_weights.pth`放到`ai-tools/example/captchaRecog-pytorch/numLetters_recognition/deploy_server/resources/weights`
	
	- 构建

	 ```
     /usr/bin/python3 setup-s.py clean --all
     ```

     ```
     /usr/bin/python3 setup-s.py build
     ```

	- 安装

     ```
     /usr/bin/python3 setup-s.py install
     ```

	- 直接运行
   	
	 ```
     recogcap-s
     ```
	
 	 参数说明：
		<table>
		  <thead>
		    <tr style="text-align: center;">
		      <th></th>
		      <th>参数名称</th>
		      <th>默认值</th>
		      <th>说明</th>
		    </tr>
		  </thead>
		  <tbody>
		    <tr>
		      <th>0</th>
		      <td>`--host`</td>
		      <td>`"127.0.0.1"`</td>
		      <td>部署的服务端的IP地址</td>
		    </tr>
		    <tr>
		      <th>1</th>
		      <td>`--port`</td>
		      <td>`5000`</td>
		      <td>部署的服务端的端口号</td>
		    </tr>
		    <tr>
		      <th>2</th>
		      <td>`--model`</td>
		      <td>`"ResNet18"`</td>
		      <td>识别时所使用的主干网络选择。要与加载的网络权重相对应，可根据不同的需求选择ResNet18/34/50/101和VGG11/13/16/19</td>
		    </tr>
			<tr>
		      <th>3</th>
		      <td>`--model_path`</td>
		      <td>(空)</td>
		      <td>网络权重的加载路径，默认加载`/root/ai-tools/recogcap/resources/weights/model_weights.pth`</td>
		    </tr>
			<tr>
		      <th>4</th>
		      <td>`--cap_array`</td>
		      <td>`"0123456789abcdefghijklmnopqrstuvwxyz"`</td>
		      <td>此参数用于指定验证码的内容，与网络的权重相对应</td>
		    </tr>
		  </tbody>
		</table>

	示例：`recogcap-s --host 127.0.0.1 --port 5000 --model ResNet18`

	- 以服务的方式运行

     ```
     systemctl start recogcap-s.service
     ```

	如果需要修改配置，可直接修改配置文件：`/root/ai-tools/recogcap/etc/recogcap-s.conf`，然后`systemctl restart recogcap-s.service`

	- 日志文件

	```
	cat /root/ai-tools/recogcap/log/recogcap-s.log
	```
	- 运行结果
	
	服务端会及时将接收的验证码图片保存到`/root/ai-tools/recogcap/resources/received_images`，并把预测结果返回给客户端，同时产生一条日志信息。

2. 基于rpm包安装运行

	- 下载rpm包

	 ```
     git clone https://gitee.com/openeuler/ai-tools.git
     ```

	- 安装
	
	 ```
     cd ai-tools/example/captchaRecog-pytorch/numLetters_recognition/dist
     ```

     ```
     yum install recogcap-s-1.0.0-1.noarch.rpm
     ```

	- 开启服务

     ```
     systemctl start recogcap-s.service
     ```
	
	如果需要修改配置，可直接修改配置文件：`/root/ai-tools/recogcap/etc/recogcap-s.conf`，然后`systemctl restart recogcap-s.service`
	
	日志和运行结果同**1.基于源码编译、安装、运行**
#### recogcap-c 验证码识别客户端部署

1. 基于源码编译、安装、运行

   - 构建
 
	 ```
     /usr/bin/python3 setup-c.py clean --all
     ```

     ```
     /usr/bin/python3 setup-c.py build
     ```

   - 安装

     ```
     /usr/bin/python3 setup-c.py install
     ```

   - 运行

     ```
     recogcap-c
     ```
	
	参数说明：
		<table>
		  <thead>
		    <tr style="text-align: center;">
		      <th></th>
		      <th>参数名称</th>
		      <th>默认值</th>
		      <th>说明</th>
		    </tr>
		  </thead>
		  <tbody>
		    <tr>
		      <th>0</th>
		      <td>`--url`</td>
		      <td>`'http://127.0.0.1:5000'`</td>
		      <td>服务端的url</td>
		    </tr>
		    <tr>
		      <th>1</th>
		      <td>`--test`</td>
		      <td>`False`</td>
		      <td>是否进行测试，如果使用该命令，则客户端程序将随机生成一张验证码图片，并保存到`/root/ai-tools/recogcap/resources/test_images`，然后自动调用服务端的服务进行预测，预测结果将显示在终端上</td>
		    </tr>
		  </tbody>
		</table>

	示例：`recogcap-c --url http://127.0.0.1:5000 --test`

2. 基于rpm包安装运行

   - 下载rpm包

	 ```
     git clone https://gitee.com/openeuler/ai-tools.git
     ```

   - 安装
 
 	 ```
     /usr/bin/pip3 install captcha
     ```

	 ```
     cd ai-tools/example/captchaRecog-pytorch/numLetters_recognition/dist
     ```

     ```
     yum install recogcap-c-1.0.0-1.noarch.rpm
     ```

   - 运行

     ```
     recogcap-c
     ```
	
	参数同**1. 基于源码编译、安装、运行**
