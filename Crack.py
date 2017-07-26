#!/usr/bin/python
#-*- coding: utf-8 -*-
import pytesseract,math,hashlib,time
import timeit,random,requests,os
from PIL import Image
from PIL import  ImageEnhance 
from PIL import  ImageFilter 
import re

Cutting = "./Cutting/"
Train = './Record/'
#letters = []


class Crack(object):

	def Cutting(self,img_name):
		#global letters
		letters = []
		img = Image.open(img_name);    
		his = img.histogram();  

		values = {}
		for i in range(0, len(his)):
		    values[i] = his[i]

		temp = sorted(values.items(),  key = lambda x: x[1], reverse = True)

		inletter= False
		foundletter= False
		start = 0
		end = 0
		img.show()

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


		count = 0
		for letter in letters:
		    img2 = img.crop((letter[0], 0, letter[1], img.size[1]))
		    #img2.save("./test/%s.png" % (count))
		    count += 1

		imageset = self.LoadTrain()
		self.CrackImg(img_name,imageset,letters)

	def magnitude(self, concordance):
	    total = 0
	    for word, count in concordance.items():
	        total += count ** 2
	    return math.sqrt(total)

	def relation(self, concordance1, concordance2):
	    topvalue = 0
	    for word, count in concordance1.items():
	        if word in concordance2:
	            topvalue += count * concordance2[word]
	    return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


	def buildvector(self,im):
	    d1 = {}
	    count = 0
	    for i in im.getdata():
	        d1[count] = i
	        count += 1
	    return d1


	def LoadTrain(self):
		import os 
		imageset = []
		iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k','l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

		imageset = []
		for letter in iconset:
		    for img in os.listdir(Train+'%s/' % (letter)):
		        temp = []
		        if img != "Thumbs.db" and img != ".DS_Store":
		            temp.append(self.buildvector(Image.open(Train+"/%s/%s" % (letter, img))))
		        imageset.append({letter: temp})
		return imageset     

	def CrackImg(self,img_name,imageset,letters):
		#global letters
		img = Image.open(img_name); 
		coutn = 0
		data = []
		for letter in letters:
		    img2 = img.crop((letter[0], 0, letter[1], img.size[1]))
		    guess = []
		    for image in imageset:
		        for x, y in image.items():
		            if len(y) != 0:
		                guess.append((self.relation(y[0], self.buildvector(img2)), x))

		    guess.sort(reverse=True)
		    data.append(guess[0][1])
		    #print(guess[0])
		    coutn += 1
		print(data)
	
if __name__ == "__main__":
	C = Crack()
	C.Cutting("./Modif/1.png")
