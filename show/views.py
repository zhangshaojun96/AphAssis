# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from upload.models import Ques, guide
from django.http import HttpResponse, JsonResponse
# Create your views here.


import datetime
import time
import os
import base64
from face.run import get_emotion
from show.models import Recom_guide

number = int(0)
questions = list(Ques.objects.all())
length = len(questions)
question = questions[number]

'''
def show(request):
	return render(request,'show/showImg.html')
'''

def index(request):
	return render(request,'show/index.html')

@csrf_exempt
def get_next(request):
	global number	
	global questions
	global length
	global question
		
	if number < length:
		question = questions[number]	
	ques = str(question.question)
	imageA = str(question.imageA)
	DesA = str(question.DesA)
	imageB = str(question.imageB)
	DesB = str(question.DesB)
	imageC = str(question.imageC)
	DesC = str(question.DesC)
	imageD = str(question.imageD)
	DesD = str(question.DesD)
	voice = str(question.voice)
	if number < length:
		number += 1
	else:
		ques = ""
	return JsonResponse({"namee":ques,
						 "imageA":imageA,
						 "DesA":DesA,
						 "imageB":imageB,
						 "DesB":DesB,
						 "imageC":imageC,
						 "DesC":DesC,
						 "imageD":imageD,
						 "DesD":DesD,
						 "voice":voice
							})


@csrf_exempt
def error_answer(request):
	right = request.POST.get('right',None)
	wrong = request.POST.get('wrong',None)	
	Guider = list(guide.objects.filter(right_answer=right,wrong_answer=wrong))
	
	if len(Guider) > 0:
		tip = random.sample(Guider,1)
		result = tip[0].tips
		return JsonResponse({"guide":result})
	else:
		tip = ""
		return JsonResponse({"guide":tip})
	


'''
表情识别
'''
# 存储用户表情识别结果
regs = []


# 前端上传摄像头截图
@csrf_exempt
def upload_snap(request):
    if request.method == 'POST':
        # 接收图片
        snap_base64 = request.POST.get('snap_base64', None)

        # 时间戳命名，保存图片，作为检验
        snap = base64.b64decode(snap_base64)
        filename = str(time.time())
        dest = "/home/ll/dev/workspace/python/AphAssis/external/snap/" + filename + ".png"
        if os.path.exists(dest):
            os.remove(dest)
        with open(dest, "wb+") as destination:
            destination.write(snap)
        print("截图保存在" + dest)
        # 分析图片，记录表情
        res = get_emotion(snap_base64)
        regs.extend(res)
        print("表情为： ")
        print(res)
        return JsonResponse({"face_reg_test": res})


# 获取表情列表
@csrf_exempt
def get_feeling(request):
    if request.method == 'POST':
        # 深拷贝
        tmp = regs[:]
        regs.clear()
        print("历史表情: ")
        print(tmp)
        return JsonResponse({"feeling": tmp})

def show(request):
	all_ques = Ques.objects.all()
	questions = list(all_ques)
	question = questions[0]
	return render(request,'show/gallery.html',{"question":question})
