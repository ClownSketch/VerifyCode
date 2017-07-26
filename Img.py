#!/usr/bin/python
#coding: utf-8

import timeit,random,time,requests,os
from PIL import Image,ImageDraw
from PIL import  ImageEnhance 
from PIL import  ImageFilter 
import pytesseract
from Crack import *



Get_path = "./img_data/"    #下载图片保存路径
Get_url = ""
Get_number = 10             #下载图片数量
Edit_path = './Edit/'       #灰度图目录
Edit_name = ''              #保存灰度图名称
Modif = './Modif/'          #去掉干扰线后保存路径
val_img = 0                 #去掉干扰线后保存名称
Cutting = './Cutting/'      #临时保存
Iconset = './Record/'      #数据存储
ico = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k','l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class IMG(object):
  
    def GetImgCode(self):
        get_img_start = time.time()
        if os.path.isdir(Get_path):
            pass
        else:
            mkdir = os.makedirs(Get_path)
            print('下载目录不存在，创建目录中----------')
            print('下载目录创建成功，目录名->'+Get_path)
        if Get_url !='':
	        print("获取下载链接成功---------")
	        print("开始下载验证码")
	        for i in range(0,Get_number):
	            print("下载第"+str(i)+"张验证码")
	            filePath = Get_path+str(i)+'.jpg'
	            Get_img = requests.get(Get_url)
	            with open(filePath,'bw') as f:
	                f.write(Get_img.content)
	        get_img_end = time.time()
	        print("已完成，共下载"+str(Get_number)+"张验证码---------")
	        print ("执行时间 %f m"%(get_img_end-get_img_start))
        
        else:
        	print('验证码下载地址为空')
        	exit()	 


    def HandleVerify(self): 
        info_len = 0
        han_img_start = time.time()
        print('开始处理图片')
        threshold = 140
        table = [] 
        for i in range(256): 
            if i < threshold: 
                table.append(0) 
            else: 
                table.append(1) 

        Img_len = os.listdir(Get_path)
        print("获取图片总数，-》"+str(len(Img_len)))
        if os.path.isdir(Edit_path):
            pass
        else:
            mkdir = os.makedirs(Edit_path)
            print('保存灰度图目录不存在，创建目录中----------')
            print('保存灰度图目录创建成功，目录名->'+Edit_path)
        for i in range(0,len(Img_len)):
            info_len+=1
            print("正在处理第"+str(i+1)+'张验证码')
            ini_time = int(time.time())
            edit_img_name = random.randint(0,ini_time)  
            img_name = str(i)+'.jpg'
            im = Image.open(Get_path+img_name)
            imgry = im.convert('L')
            out = imgry.point(table,'1') 
            Edit_name = Edit_path+str(edit_img_name)+'.jpg'    
            out.save(Edit_name) 
            self.resize_img(Edit_name)
            #self.ModifyImg(Edit_name)
        han_img_end = time.time()
        print ("图片转换完成，耗时 %f m， 共转换 %s 张"%(han_img_end-han_img_start,info_len))



    def ModifyImg(self,img_name):
        global val_img
        val_img+=1
        if val_img <= 1:
            print('准备去除验证码干扰线----------')
            if os.path.isdir(Modif):
                pass
            else:
                mkdir = os.makedirs(Modif)
                print('保存去除验证码图片目录不存在，创建目录中----------')
                print('保存去除验证码图片目录创建成功，目录名->'+Modif)
        else:
            pass

        img = Image.open(img_name)
        img = img.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.convert('1')

        width, height = img.size
        data = []
        for i in range(height):
            tmp=[]
            for j in range(width):
                if(img.getpixel((j,i)) == 255 ):
                    tmp.append(1)
                else:
                    tmp.append(0)
            data.append(tmp)
              
        img2 = Image.new("P",img.size, 255)
        for y in range(height):
            for a in range(len(data[y])):
                
                o = y+1
                t = y+2
                #s = y+3
                z = a+1
                x = a+2
                try:
                    if data[o][a] == 0 and data[t][a] == 0 and data[y][z] == 0  and data[y][x] == 0:#and data[s][a] == 0 
                        img2.putpixel((a,y),1)
                        img2.save(Modif+str(val_img)+'.png')
                        
                        
                except:
                    pass
        img2_path = Modif+str(val_img)+'.png'

        image = Image.open(img2_path)  
        image = image.convert("L")  
        self.clearNoise(image,53,4,8)  
        image.save(img2_path)  
        image.show()
        self.ImgCutting(img2_path)
        

    def ImgCutting(self,img_name):
        global val_img
        if val_img <=1:
            if os.path.isdir(Cutting):
                pass
            else:
                mkdir = os.makedirs(Cutting)
                print('临时保存目录不存在，创建目录中----------')
                print('临时保存图目录创建成功，目录名->'+Cutting)

        inletter= False
        foundletter= False
        start = 0
        end = 0
        letters = []

        img = Image.open(img_name)
        his = img.histogram();

        values = {}
        for i in range(0, len(his)):
            values[i] = his[i]

        temp = sorted(values.items(),  key = lambda x: x[1], reverse = True)

        for x in range(img.size[0]):
            for y in range(img.size[1]):
                pix = img.getpixel((x,y))
                if pix != 255:
                    inletter = True
            if foundletter  == False and inletter == True:
                foundletter = True
                start = x

            if foundletter == True and inletter == False:
                foundletter = False
                end = x
                letters.append((start,end))

            inletter = False
        
        for letter in letters:
            ini_time = int(time.time())
            code_img_name = random.randint(0,ini_time)
            img2 = img.crop((letter[0], 0, letter[1], img.size[1]))
            save_path = Cutting+str(code_img_name)+'.png'
            img2.save(save_path)
   
    def resize_img(self,img_path):
        img= Image.open(img_path)
        width,height = img.size
        new_width = 280
        new_height = int(height * new_width / width)
        out = img.resize((new_width,new_height),Image.ANTIALIAS)
        ext = os.path.splitext(img_path)[1]
        out.save(img_path,quality=95)    
        self.ModifyImg(img_path)


    def getPixel(self,image,x,y,G,N):  
        L = image.getpixel((x,y))  
        if L > G:  
            L = True  
        else:  
            L = False  
      
        nearDots = 0  
        if L == (image.getpixel((x - 1,y - 1)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x - 1,y)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x - 1,y + 1)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x,y - 1)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x,y + 1)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x + 1,y - 1)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x + 1,y)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x + 1,y + 1)) > G):  
            nearDots += 1  
      
        if nearDots < N:  
            return image.getpixel((x,y-1))  
        else:  
            return None  

    def clearNoise(self,image,G,N,Z):  
        draw = ImageDraw.Draw(image)  
      
        for i in range(0,Z):  
            for x in range(1,image.size[0] - 1):  
                for y in range(1,image.size[1] - 1):  
                    color = self.getPixel(image,x,y,G,N)  
                    if color != None:  
                        draw.point((x,y),color)         

    def Class_dir(self):
        for j in range(len(ico)):
            file_name = Iconset+str(ico[j])
            os.mkdir(file_name)

if __name__ == '__main__':
    Img = IMG()
    #Img.GetImgCode()
    Img.HandleVerify()
    #Img.Class_dir()
    
