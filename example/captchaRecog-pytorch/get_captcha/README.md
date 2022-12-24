# getcap
#### 介绍
getcap是一个验证码生成库，目的是为其他开发人员提供验证码识别过程需要的验证码数据集，目前包括纯数字、纯字母、数字字母组合、数字运算（+、-、x）、滑块拖拽、物体识别和图片旋转这几类验证码的自动生成，另外还有一个用来在网络上爬取图片的方法类。

- **GetCaptcha**
	- 这是一个验证码生成类，其中包含纯数字、纯字母、数字字母组合、数字运算（+、-、x）、滑块拖拽、物体识别和图片旋转这几类验证码的自动生成方法：
		- `get_number_and_letter()`
		- `get_pure_letter()`
		- `get_pure_number()`
		- `get_number_operations()`
		- `get_behavior_drag()`
		- `get_behavior_rotate()`
		- `get_behavior_object_recognition()`

- **BingImagesSpider**
	- 这是一个从网上爬取图片的方法类，可作为验证码生成过程中的一些图片素材的来源。

#### 环境

- 安装python3
- 为了更好的管理项目，建议使用venv:`python3 -m venv venv && source venv/bin/active`
- 执行命令`pip install -r requirements.txt`安装依赖模块

#### 安装
1.  `git clone https://gitee.com/openeuler/ai-tools.git`
2.  在 `ai-tools/example/。。。 `文件夹下执行如下命令
3.  `python3 setup.py build`
4.  `python3 setup.py install`
#### 使用
1. 使用方法：`from getcap.get_captcha import GetCaptcha，BingImagesSpider`
	- 在根目录下创建`datasets`文件夹
	- BingImagesSpider爬取图片： `BingImagesSpider('人行街道', 5, 'datasets').run()`
	- GetCaptcha生成验证码图片：
		- 生成数字与字母组合的验证码：`GetCaptcha().get_number_and_letter("datasets",num=5,num_img=5)`

3. 使用示例：`ai-tools/example/。。。 `文件夹下执行`python test.py`
4. 验证码结果命名规则：
	- `get_number_and_letter()`：`真值_序号.png`
	- `get_pure_letter()`：`真值_序号.png`
	- `get_pure_number()`：`真值_序号.png`
	- `get_number_operations()`：`序号_真值.png`
	- `get_behavior_drag()`：`back/shape_序号_缺口横坐标_缺口纵坐标.png`
	- `get_behavior_rotate()`：`输入图片名_ro_旋转角度(逆时针).png`
	- `get_behavior_object_recognition()`：`输入图片名_序号_是否包含目标物体(t/f).png`