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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from show.models import wrong_record
from show.Collaborative_filtering.sim import  collaborative_filtering

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
wrong_q = []
wrong_pair = {}


def index(request):
    username = request.session['username']
    classid = request.session['classid']
    userid = request.session['userid']
    return render(request, 'show/index.html',
                  {'userid': userid, 'username': username, 'classid': classid})


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

        #print("表情为： ")
        #print(res)
        return JsonResponse({"face_reg_test": res})
    # return JsonResponse({"face_reg_test": []})


# 获取表情列表
@csrf_exempt
def get_feeling(request):
    if request.method == 'POST':
        # 深拷贝
        tmp = regs[:]
        regs.clear()
        ##print("历史表情: ")
        ##print(tmp)
        if len(tmp) == 0:
            tmp = [0]
        return JsonResponse({"feeling": tmp})


# 显示套题详情
def set_detail(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        m = QuestionSet.objects.get(id=id)
        if m:
            questions = list()
            questions_id = m.questions.split(',')
            for quesid in questions_id:
                ques = Ques.objects.get(id=quesid)
                ques.imageA = '/media/' + ques.imageA.__str__()
                ques.imageB = '/media/' + ques.imageB.__str__()
                ques.imageC = '/media/' + ques.imageC.__str__()
                ques.imageD = '/media/' + ques.imageD.__str__()
                questions.append(ques)

            count = len(questions)
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

            return render(request, 'show/showSetDetail.html',
                          {'posts': posts, 'username': username, 'classid': classid, 'setid': id})
        else:
            return render(request, 'login/login.html')


# 显示全部题目
def showAllEx(request):
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


# 套题的分配
def setArrange(request):
    # 获取全部的患者
    patients = list(register.objects.filter(res_id=0))
    username = request.session['username']
    classid = request.session['classid']
    return render(request, 'show/setArrange.html',
                  {'username': username, 'classid': classid, 'patients': patients})


# 所有套题
def setDisplay(request):
    sets = list(QuestionSet.objects.all())
    setlist = []

    for item in sets:
        tmp = {}
        tmp['id'] = item.id
        tmp['setDes'] = item.setDes
        tmp['count'] = len(str(item.questions).split(','))
        tmp['questions'] = str(item.questions).split(',')
        tmp['href'] = '/set_detail?id=' + str(item.id)
        setlist.append(tmp)
    # 使用分页组件  分页显示

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


# 获取全部的套题
def get_allSets(request):
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
    arrid = request.GET.get('id')
    username = request.session['username']
    userid = request.session['userid']
    classid = request.session['classid']
    print('do ex set id: ' + str(setid))
    return render(request, 'show/doEx.html',
                  {'userid': userid, 'username': username, 'classid': classid, 'arrid': arrid, 'setid': setid})


@csrf_exempt
def error_answer(request):
    error_no = request.POST.get('no', None)

    # 协同过滤需要的参数
    ques_id = questions[int(error_no) - 1].id  # 得到绝对问题id
    user_id = request.POST.get('user_id', None)
    wrong_answer = request.POST.get('wrong_choice_id', None)

    # 保存用户完整的答错题过程
    setid = request.POST.get("setid", None)
    arrid = request.POST.get("arrid", None)
    current_ques_id = request.POST.get('cur_ques_id', None)
    current_wrong_option = request.POST.get('current_wrong_option', None)

    if str(error_no) not in wrong_q:
        wrong_q.append(str(error_no))  # 用来保存顺序
    if str(error_no) not in wrong_pair:
        wrong_pair[str(error_no)] = ''  # 用来保存错题-错误选项-有效引导语  对

    right = request.POST.get('right', None)
    wrong = request.POST.get('wrong', None)
    Guider = list(guide.objects.filter(right_answer=right, wrong_answer=wrong))

    if len(Guider) > 0:
        ###算法调用
        ### 1, collab filter
        collab_tip_id=collaborative_filtering(user_id,ques_id,current_wrong_option)
        if collab_tip_id is not None:
            recom_guide_id=collab_tip_id
            # 查具体引导语信息
            result=guide.objects.get(id=recom_guide_id).tips
        else:
            ### 2, 多臂老虎机
            ### 3，random



            tip = random.sample(Guider, 1)
            print('random guide id :'+tip[0].id)
            recom_guide_id=tip[0].id
            result = tip[0].tips
        # 完善答错题记录
        if current_ques_id != -1:
            # 查找错题号码，追加 错选项-引导语的id
            wrong_pair[str(current_ques_id)] += str(current_wrong_option) + str('#') + str(recom_guide_id) + str('<')

        return JsonResponse({"guide": result, 'id': recom_guide_id})
    else:
        tip = ""
        # 完善答错题记录
        if current_ques_id != -1:
            # 查找错题号码，追加 错选项-引导语的id
            wrong_pair[str(current_ques_id)] += str(current_wrong_option) + str('#') + str(-1) + str('<')
        return JsonResponse({"guide": tip, 'id': -1})


# 获取指定id的套题的题目的下一道题
@csrf_exempt
def get_nextToDo(request):
    # print('get next to do......')
    global number
    global questions
    global length
    global question
    global wrong_q

    user_id = request.POST.get("user_id", None)
    setid = request.POST.get("setid", None)
    arrid = request.POST.get("arrid", None)
    # 协同过滤需要保存的参数
    current_ques_id = request.POST.get('cur_ques_id', None)
    current_valid_guide_id = request.POST.get('cur_valid_guide_id', None)
    current_valid_guide_path = request.POST.get('current_valid_guide_path', None)
    current_wrong_option = request.POST.get('current_wrong_option', None)

    print("current set id : " + str(setid))
    typeid = request.POST.get("type", None)  # type==0  初始化

    if int(typeid) == 0:
        # print('get next to do......init ')
        ques_set = QuestionSet.objects.get(id=setid)
        ques_list = ques_set.questions.split(',')
        length = len(ques_list)
        for ques_id in ques_list:
            ques = Ques.objects.get(id=ques_id)
            questions.append(ques)

    current_ques_id = questions[int(current_ques_id) - 1].id  # 得到绝对问题id
    # print('get next to do......next')
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
        # print('number : ' + str(number))
        # print('length : ' + str(length))

    # 新办法 记录每道题目的最后一个答错选项-引导语id
    if int(current_wrong_option) != -1 and len(current_valid_guide_path) != 0:
        wrong_item = wrong_record(
            userid=user_id,
            question_id=current_ques_id,
            wrong_choice=current_wrong_option,
            guide=current_valid_guide_id
        )
        wrong_item.save()

    if number < length:
        number += 1
    else:
        # print("store start")
        time_used = request.POST.get("time", None)
        w_str = ''
        # 保存全部答错题记录
        for ques_id in wrong_q:
            # print('fake ques id' + str(ques_id))
            # print('true ques id' + str(questions[int(ques_id) - 1].id))

            wrong_chice_guide_pairs = wrong_pair[ques_id]
            if wrong_chice_guide_pairs.endswith('<'):
                wrong_chice_guide_pairs = wrong_chice_guide_pairs[0:len(wrong_chice_guide_pairs) - 1]
            w_str += str(questions[int(ques_id) - 1].id) + '@' + str(wrong_chice_guide_pairs) + str(',')
        if w_str.endswith(','):
            w_str = w_str[0:len(w_str) - 1]

        arrange = Arrange_set.objects.get(id=arrid)
        arrange.usedTime = time_used
        arrange.finTime = datetime.datetime.now()
        arrange.wrong_ques = w_str
        arrange.status = 1
        arrange.save()

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
    # print('current user id ": ' + str(userid))
    arrs = list(Arrange_set.objects.filter(userid=userid, status=1).order_by("-arrTime"))
    length = len(arrs)
    ans = {}
    ans["length"] = length
    for i in range(length):
        ans['id' + str(i)] = str(arrs[i].id)
        ans['setdes' + str(i)] = QuestionSet.objects.get(id=arrs[i].set).setDes
        ans["arr_set" + str(i)] = str(arrs[i].set)
        dt_arr = arrs[i].arrTime.strftime("%Y/%m/%d %H:%M:%S")
        dt_fin = arrs[i].finTime.strftime("%Y/%m/%d %H:%M:%S")
        ans["arr_datetime" + str(i)] = str(dt_arr)
        ans["fin_datetime" + str(i)] = str(dt_fin)
        ans["used_time" + str(i)] = str(arrs[i].usedTime) + '秒'
        ans["arr_userid" + str(i)] = str(arrs[i].userid)
    # toList.append(deepcopy(ans))
    return JsonResponse(ans)


# 获取要做的所有任务
def get_allMyToDoSet(request):
    userid = request.session['userid']
    # print('current user id ": ' + str(userid))
    arrs = list(Arrange_set.objects.filter(userid=userid, status=0).order_by("-arrTime"))
    length = len(arrs)
    ans = {}
    ans["length"] = length
    for i in range(length):
        ans['id' + str(i)] = str(arrs[i].id)
        ans['setdes' + str(i)] = QuestionSet.objects.get(id=arrs[i].set).setDes
        ans["arr_set" + str(i)] = str(arrs[i].set)
        dt_new = arrs[i].arrTime.strftime("%Y/%m/%d %H:%M:%S")
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


# 显示患者的详细信息
def gen_detail(request):
    need_gen_str = request.GET.get('id')
    need_gen_no = int(need_gen_str)
    all_sets = QuestionSet.objects.all()
    need_gen = register.objects.get(res_id=0,id=need_gen_no) # 获取患者
    print('show gen id : '+str(need_gen.id))
    sets = list(Arrange_set.objects.filter(userid=need_gen.id))  # 获取这个人对应的所有套题
    # print("len %d\n",len(sets))
    detail = []
    # 下面是患者在每套题的情况
    for item in sets:
        temp = {}
        if item.status == 0:
            temp['status'] = '未完成'
            temp["time"] = '--'
            temp["wrong"] = '--'
            temp["fintime"] = '--'
        else:
            temp['status'] = '已完成'
            temp["time"] = str(item.usedTime) + '秒'

            #解析错题记录
            w_list = str(item.wrong_ques).split(',')
            w_str = ''
            for wrong_pair in w_list:
                ls = str(wrong_pair).split('@')
                wrong_ques_id = ls[0]
                wrong_log = ls[1]
                w_str += str(wrong_ques_id) + ','
            if w_str.endswith(','):
                w_str = w_str[0:len(w_str) - 1]
            if len(w_str) > 10:
                w_str = w_str[0:6]
                w_str = w_str + ".."
            temp["wrong"] = w_str
            temp['fintime'] = item.finTime.strftime("%Y/%m/%d %H:%M:%S")

        # print(len(all_sets.filter(setId=item.set)))
        temp["name"] = all_sets.filter(id=item.set)[0].setDes
        temp["arrtime"] = item.arrTime.strftime("%Y/%m/%d %H:%M:%S")
        detail.append(temp)

    print("show gen detail len: "+str(len(detail)))
    current_page = request.GET.get('p')
    # Paginator对象，里面封装了上面那些值，把USER_LIST对象传过来了，显示10页
    paginator = Paginator(detail, 3)

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
    return render(request, 'show/genDetail.html', {'posts': posts,'genid':need_gen_no, 'username': username, 'classid': classid})


# 所有患者
def allGen(request):
    gens = list(register.objects.filter(res_id=0))
    # genList = []
    # for item in gens:
    #     temp = {}
    #     temp['id'] = i
    #     temp['name'] = item.res_username
    #     genList.append(temp)
    #     i = i + 1

    current_page = request.GET.get('p')
    # Paginator对象，里面封装了上面那些值，把USER_LIST对象传过来了，显示10页
    paginator = Paginator(gens, 3)

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
    return render(request, 'show/allGen.html', {'posts': posts, 'username': username, 'classid': classid})


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
    # print(patientid)

    for i in l:
        new_arr = Arrange_set(
            userid=int(patientid),
            set=i
        )
        new_arr.save()

    return JsonResponse({"status": 1})
