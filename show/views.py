# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from upload.models import Ques, guide
from show.models import Arrange_set
from makeSet.models import QuestionSet
from login.models import register
from django.http import HttpResponse, JsonResponse
import datetime, time
# Create your views here.


import datetime
import time
import os
import base64
from face.run import get_emotion
from show.models import Recom_guide

# 全局变量
number = int(0)
questions = []
length = 0
question = None

'''
def show(request):
	return render(request,'show/showImg.html')
'''


def index(request):
    return render(request, 'show/index.html')


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
    return JsonResponse({"namee": ques,
                         "imageA": imageA,
                         "DesA": DesA,
                         "imageB": imageB,
                         "DesB": DesB,
                         "imageC": imageC,
                         "DesC": DesC,
                         "imageD": imageD,
                         "DesD": DesD,
                         "voice": voice
                         })


@csrf_exempt
def error_answer(request):
    right = request.POST.get('right', None)
    wrong = request.POST.get('wrong', None)
    Guider = list(guide.objects.filter(right_answer=right, wrong_answer=wrong))

    if len(Guider) > 0:
        tip = random.sample(Guider, 1)
        result = tip[0].tips
        return JsonResponse({"guide": result})
    else:
        tip = ""
        return JsonResponse({"guide": tip})


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

        # # 时间戳命名，保存图片，作为检验
        # snap = base64.b64decode(snap_base64)
        # filename = str(time.time())
        # dest = "/home/ll/dev/workspace/python/AphAssis/external/snap/" + filename + ".png"
        # if os.path.exists(dest):
        #     os.remove(dest)
        # with open(dest, "wb+") as destination:
        #     destination.write(snap)
        # print("截图保存在" + dest)
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
        if len(tmp) == 0:
            tmp = [0]
        return JsonResponse({"feeling": tmp})


# def show(request):
#     all_ques = Ques.objects.all()
#     questions = list(all_ques)
#     question = questions[0]
#     username = request.session['username']
#     classid = request.session['classid']
#
#     return render(request, 'show/gallery.html', {"question": question,'username': username,'classid': classid})


def show(request):
    all_ques = Ques.objects.all()
    questions = list(all_ques)
    for ques in questions:
        ques.imageA = '/media/' + ques.imageA.__str__()
        ques.imageB = '/media/' + ques.imageB.__str__()
        ques.imageC = '/media/' + ques.imageC.__str__()
        ques.imageD = '/media/' + ques.imageD.__str__()
    count = all_ques.count()
    # 使用分页组件  分页显示
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    # 全部数据:USER_LIST,=>得出共有多少条数据
    # per_page: 每页显示条目数量
    # count:    数据总个数
    # num_pages:总页数
    # page_range:总页数的索引范围，如: (1,10),(1,200)
    # page:     page对象 (是否具有下一页，是否有上一页)

    current_page = request.GET.get('p')
    # Paginator对象，里面封装了上面那些值，把USER_LIST对象传过来了，显示10页
    paginator = Paginator(questions, 3)
    try:
        # page对象
        # posts配置对象(current_page用户可能填些不合法的字段）
        # paginator通过拿到了page对象，把current_page传进来
        posts = paginator.page(current_page)
        # has_next              是否有下一页
        # next_page_number      下一页页码
        # has_previous          是否有上一页
        # previous_page_number  上一页页码
        # object_list           分页之后的数据列表,已经切片好的数据
        # number                当前页
        # paginator             paginator对象

    # 表示你填的东西不是个整数
    except PageNotAnInteger:
        posts = paginator.page(1)
    # 空页的时候，表示你看完了，显示最后一页
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    username = request.session['username']
    classid = request.session['classid']

    return render(request, 'show/showAllEx.html', {'posts': posts, 'username': username, 'classid': classid})


# # 所有套题
# def setDisplay(request):
#     sets = list(QuestionSet.objects.all())
#     username = request.session['username']
#     classid = request.session['classid']
#     return render(request, 'show/allSet.html', {'username': username, 'classid': classid})

# 所有套题
def setDisplay(request):
    sets = list(QuestionSet.objects.all())
    setlist = []

    for item in sets:
        tmp = {}
        tmp['id'] = item.setId
        tmp['setDes'] = item.setDes
        tmp['count'] = len(str(item.questions).split(','))
        tmp['questions'] = str(item.questions).split(',')
        setlist.append(tmp)
    # 使用分页组件  分页显示
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    # 全部数据:USER_LIST,=>得出共有多少条数据
    # per_page: 每页显示条目数量
    # count:    数据总个数
    # num_pages:总页数
    # page_range:总页数的索引范围，如: (1,10),(1,200)
    # page:     page对象 (是否具有下一页，是否有上一页)

    current_page = request.GET.get('p')
    # Paginator对象，里面封装了上面那些值，把USER_LIST对象传过来了，显示10页
    paginator = Paginator(setlist, 3)
    try:
        # page对象
        # posts配置对象(current_page用户可能填些不合法的字段）
        # paginator通过拿到了page对象，把current_page传进来
        posts = paginator.page(current_page)
        # has_next              是否有下一页
        # next_page_number      下一页页码
        # has_previous          是否有上一页
        # previous_page_number  上一页页码
        # object_list           分页之后的数据列表,已经切片好的数据
        # number                当前页
        # paginator             paginator对象

    # 表示你填的东西不是个整数
    except PageNotAnInteger:
        posts = paginator.page(1)
    # 空页的时候，表示你看完了，显示最后一页
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    username = request.session['username']
    classid = request.session['classid']
    return render(request, 'show/showAllSet.html', {'posts': posts, 'username': username, 'classid': classid})


# 套题的分配
def setArrange(request):
    # 获取全部的套题
    # sets = list(QuestionSet.objects.all())
    # setlist = []
    #
    # for item in sets:
    #     tmp = {}
    #     tmp['id'] = item.setId
    #     tmp['setDes'] = item.setDes
    #     tmp['count'] = len(str(item.questions).split(','))
    #     tmp['questions'] = str(item.questions).split(',')
    #     setlist.append(tmp)

    # 获取全部的患者
    patients = list(register.objects.filter(res_id=0))
    username = request.session['username']
    classid = request.session['classid']
    return render(request, 'show/setArr.html',
                  {'username': username, 'classid': classid, 'patients': patients})


def get_allSets(request):
    # 获取全部的套题
    sets = list(QuestionSet.objects.all())

    ans = {}
    ans['length'] = len(sets)

    for i in range(ans['length']):
        ans["id" + str(i)] = str(sets[i].id)
        ans["setDes" + str(i)] = str(sets[i].setDes)
        ans["count" + str(i)] = str(len(str(sets[i].questions).split(',')))
        ans["questions" + str(i)] = str(sets[i].questions)

    return JsonResponse(ans)


# 训练
def doEx(request):
    setid = request.GET.get('setid')
    username = request.session['username']
    classid = request.session['classid']
    print('do ex set id: ' + str(setid))
    return render(request, 'show/doEx.html', {'username': username, 'classid': classid, 'setid': setid})


# 获取指定id的套题的题目的下一道题
@csrf_exempt
def get_nextToDo(request):
    print('get next to do......')
    global number
    global questions
    global length
    global question

    setid = request.POST.get("setid", None)
    print("current set id : " + str(setid))
    typeid = request.POST.get("type", None)  # type==0  初始化
    if int(typeid) == 0:
        print('get next to do......init ')
        ques_set = QuestionSet.objects.get(id=setid)
        ques_list = ques_set.questions.split(',')
        length = len(ques_list)
        for ques_id in ques_list:
            ques = Ques.objects.get(id=ques_id)
            questions.append(ques)
    print('get next to do......next')
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
    print('number : ' + str(number))
    print('length : ' + str(length))
    if number < length:
        number += 1
    else:
        number = 0
        length = 0
        questions = []
        question = None

        ques = ""
        imageA = ""
        DesA = ""
        imageB = ""
        DesB = ""
        imageC = ""
        DesC = ""
        imageD = ""
        DesD = ""
        voice = ""
    return JsonResponse({"namee": ques,
                         "imageA": imageA,
                         "DesA": DesA,
                         "imageB": imageB,
                         "DesB": DesB,
                         "imageC": imageC,
                         "DesC": DesC,
                         "imageD": imageD,
                         "DesD": DesD,
                         "voice": voice
                         })


# 获取已经完成的所有任务
def get_allMyDoneSet(request):
    userid = request.session['userid']
    print('current user id ": ' + str(userid))
    arrs = list(Arrange_set.objects.filter(userid=userid, status=1).order_by("-dateTime"))
    length = len(arrs)
    ans = {}
    ans["length"] = length
    for i in range(length):
        ans['id' + str(i)] = str(arrs[i].id)
        ans['setdes' + str(i)] = QuestionSet.objects.get(id=arrs[i].set).setDes
        ans["arr_set" + str(i)] = str(arrs[i].set)
        dt_new = arrs[i].dateTime.strftime("%Y/%m/%d %H:%M:%S")
        ans["arr_datetime" + str(i)] = str(dt_new)
        ans["arr_userid" + str(i)] = str(arrs[i].userid)
    # toList.append(deepcopy(ans))
    return JsonResponse(ans)


# 获取要做的所有任务
def get_allMyToDoSet(request):
    userid = request.session['userid']
    print('current user id ": ' + str(userid))
    arrs = list(Arrange_set.objects.filter(userid=userid, status=0).order_by("-dateTime"))
    length = len(arrs)
    ans = {}
    ans["length"] = length
    for i in range(length):
        ans['id' + str(i)] = str(arrs[i].id)
        ans['setdes' + str(i)] = QuestionSet.objects.get(id=arrs[i].set).setDes
        ans["arr_set" + str(i)] = str(arrs[i].set)
        dt_new = arrs[i].dateTime.strftime("%Y/%m/%d %H:%M:%S")
        ans["arr_datetime" + str(i)] = str(dt_new)
        ans["arr_userid" + str(i)] = str(arrs[i].userid)
    # toList.append(deepcopy(ans))
    return JsonResponse(ans)


# 显示要做的的任务
def view_allMyToDoSet(request):
    username = request.session['username']
    classid = request.session['classid']

    return render(request, 'show/showMyToDoSet.html', {'username': username, 'classid': classid})


# 显示已经完成的任务
def view_allMyDoneSet(request):
    username = request.session['username']
    classid = request.session['classid']

    return render(request, 'show/showMyDoneSet.html', {'username': username, 'classid': classid})


# 所有患者
def allGen(request):
    username = request.session['username']
    classid = request.session['classid']
    return render(request, 'show/allGen.html', {'username': username, 'classid': classid})


def get_allGen(request):
    Gen = list(register.objects.filter(res_id=0))
    length = len(Gen)
    ans = {}
    ans["length"] = length
    for i in range(length):
        ans["gen" + str(i)] = str(Gen[i].res_username)
    # toList.append(deepcopy(ans))
    return JsonResponse(ans)


@csrf_exempt
def submit_arr(request):
    l = request.POST.get("setsCheck", None).split(',')
    patientid = request.POST.get("userid", None)
    for i in l:
        new_arr = Arrange_set(
            userid=int(patientid),
            set=i
        )
        new_arr.save()

    return JsonResponse({"status": 1})
