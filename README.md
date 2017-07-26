# VerifyCode
使用Python给图片去干扰线和噪点

Img.py     处理验证码，对验证码进行去燥，分割 <br>
Crack.py   破解验证码，得到验证码数据			<br>
此程序运行在Python3.5版本上，不是Python3请更新Python版本或更改代码，<br>
缺少需要的模块请自行下载，需要的模块可以直接用 pip install 模块名直接下载<br>

初始化程序，<br>
![image](https://raw.githubusercontent.com/Guardiant/VerifyCode/master/test_code/1.png)

如果没有测试图片，可执行GetImgCode方法获取图片，自定义下载验证码地址
![image](https://raw.githubusercontent.com/Guardiant/VerifyCode/master/test_code/4.png)

简单的干扰线去除效果还算可以，干扰线去的还算干净

![image](https://raw.githubusercontent.com/Guardiant/VerifyCode/master/test_code/2.png)

↓↓↓↓↓↓↓↓↓这是原图↓↓↓↓↓↓↓↓↓

![image](https://raw.githubusercontent.com/Guardiant/VerifyCode/master/test_code/5.png)

↓↓↓↓↓↓↓↓↓但是几条干扰线离的太进，就出现问题了↓↓↓↓↓↓↓↓↓
![image](https://raw.githubusercontent.com/Guardiant/VerifyCode/master/test_code/3.png)

↓↓↓↓↓↓↓↓↓这是原图↓↓↓↓↓↓↓↓↓
![image](https://raw.githubusercontent.com/Guardiant/VerifyCode/master/test_code/6.png)

我在这里是通过生成数据模型，在通过python的图形算法获取最邻图片的值，但数据不怎么准确，如果你们在工作上需要，可以先去除干扰线，在通过训练谷歌的Tesseract OCR来获取更精确的数据，训练Tesseract OCR的时候，需要人工辅助，如果你是大牛，可以写脚本自动辅助

↓↓↓↓↓↓↓↓↓下面是我的测试图↓↓↓↓↓↓↓↓↓
![image](https://raw.githubusercontent.com/Guardiant/VerifyCode/master/test_code/7.png)
![image](https://raw.githubusercontent.com/Guardiant/VerifyCode/master/test_code/8.png)
![image](https://raw.githubusercontent.com/Guardiant/VerifyCode/master/test_code/9.png)

可以看得出来，最后一张多了一个8，这是因为干扰线的关系，去除的不是很干净，在这里我识别的方法是把获取到的数据，和我数据模型里面的数据进行匹配，找到最邻的值，对比图上面有一个小点，我这边的模型里面有个数字8和他很相似，但是，对于这样的问题，通过Tesseract OCR训练识别的话是可以忽略的，如果你数据量挺大，最好使用脚本辅助训练