import base64
import os
import random
import time

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# 存储用户表情识别结果
regs = []


# 首页
def index(request):
    return render(request, 'faceReg/index.html')


# 前端上传摄像头截图
@csrf_exempt
def upload_snap(request):
    if request.method == 'POST':
        # 接收图片
        snap_base64 = request.POST.get('snap_base64', None)
        snap = base64.b64decode(snap_base64)
        # 时间戳命名，保存图片，作为检验
        filename = str(time.time())
        #dest = "/home/stones/source/git/AphAssis/external/" + filename + ".png"
        dest = "external/" + filename + ".png"
        if os.path.exists(dest):
            os.remove(dest)
        with open(dest, "wb+") as destination:
            destination.write(snap)
        #print("截图保存在" + dest)
        # 分析图片，记录表情，这里只是模拟收到即可
        random.seed(time.time())
        res = random.randint(-1, 1)
        regs.append(res)
        #print("表情为： " + str(res))
        #print("list: ")
        #print(regs)
        return JsonResponse({"face_reg": str(res)})

# 获取表情列表
@csrf_exempt
def get_feeling(request):
    if request.method == 'POST':
        # 深拷贝
        tmp=regs[:]
        regs.clear()
        ##print("历史 list: ")
        ##print(tmp)
        return JsonResponse({"feeling": tmp})
