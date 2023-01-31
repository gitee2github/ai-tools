## 快速部署
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

	链接：`https://pan.baidu.com/s/1pwnqq14rhQyR549-3qbEdg`， 提取码：`ikuu`

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
		      <td>`"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"`</td>
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

	- 使用自己训练的权重文件

	只需修改`--model_path`为自己的权重文件路径即可，例如`/root/ai-tools/recogcap/resources/weights/model_weights.pth`，然后修改模型对应的参数`--model`和`--cap_array`即可。

2. 基于rpm包安装运行

	- 生成rpm包
	
		1）安装rpmbuild工具，生成rpmbuild相关目录
	
		```
		yum install rpmdevtools
		```
	
		```
		yum install -y rpm-build
		```
	
		```
		rpmdev-setuptree
		```
		
		默认情况下，生成的rpmbuild相关目录在`/root/rpmbuild`
		
		2）放置源码文件及.spec文件
	
		```
		/usr/bin/python3 setup-s.py sdist --formats=gztar
		```
		
		将生成的`dist/recogcap-s-1.0.0.tar.gz`拷贝到`/root/rpmbuild/SOURCES`，将`deploy_server/rpm/recogcap-s.spec`拷贝到`/root/rpmbuild/SPECS`
		
		3）打包

		```
		rpmbuild -ba /root/rpmbuild/SPECS/recogcap-s.spec
		```
		
		生成的.rpm包在`/root/rpmbuild/RPMS`
		

	- 下载rpm包

	 链接：`https://pan.baidu.com/s/1pwnqq14rhQyR549-3qbEdg` 提取码：`ikuu`

	- 安装

     ```
     yum install recogcap-s-1.0.0-1.noarch.rpm
     ```

	- 开启服务

     ```
     systemctl start recogcap-s.service
     ```
	
	如果需要修改配置，可直接修改配置文件：`/root/ai-tools/recogcap/etc/recogcap-s.conf`，然后`systemctl restart recogcap-s.service`

	- 使用自己训练的权重文件

	只需修改配置文件：`/root/ai-tools/recogcap/etc/recogcap-s.conf`中`model_path=`自己的权重文件路径即可，例如`/root/ai-tools/recogcap/resources/weights/model_weights.pth`，然后修改模型对应的参数`model`和`cap_array`项即可。
	
	- 日志和运行结果
	
	同**1.基于源码编译、安装、运行**
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

	- 生成rpm包

	同 **recogcap-s 验证码识别服务端部署**

	- 下载rpm包


	链接：`https://pan.baidu.com/s/1pwnqq14rhQyR549-3qbEdg` 
	提取码：`ikuu`

   - 安装
 
 	 ```
     /usr/bin/pip3 install captcha
     ```

     ```
     yum install recogcap-c-1.0.0-1.noarch.rpm
     ```

   - 运行

     ```
     recogcap-c
     ```
	
	参数同**1. 基于源码编译、安装、运行**
