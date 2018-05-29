# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from upload.models import Ques
from upload.models import guide
from aip import AipSpeech

APP_ID = '11055836'
API_KEY = 'lwEPvnwUvc2thvOY9G0IkqjV'
SECRET_KEY = 'GgEGZCZY9qkRP3m8b8bnTNNWcnO3N6qS'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# Create your views here.
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        ques_str = request.POST.get('question', None)
        result = client.synthesis(ques_str, 'zh', 1, {
            'vol': 5,
        })
        if not isinstance(result, dict):
            with open("media/voice/" + ques_str + '.mp3', 'wb') as f:
                f.write(result)

        new_Ques = Ques(
            question=ques_str,
            imageA=request.FILES.get('imageA'),
            DesA=request.POST.get('desA', None),
            imageB=request.FILES.get('imageB'),
            DesB=request.POST.get('desB', None),
            imageC=request.FILES.get('imageC'),
            DesC=request.POST.get('desC', None),
            imageD=request.FILES.get('imageD'),
            DesD=request.POST.get('desD', None),
            voice="media/voice/" + ques_str + '.mp3'
        )
        new_Ques.save()
    username = request.session['username']
    classid = request.session['classid']
    return render(request, 'upload/upload1.html', {'username': username, 'classid': classid})


@csrf_exempt
def guide_upload(request):
    if request.method == 'POST':
        right = request.POST.get('right', None)
        wrong = request.POST.get('wrong', None)
        guidance = request.POST.get('guide', None)

        guide_voice = client.synthesis(guidance, 'zh', 1, {
            'vol': 5,
        })

        if not isinstance(guide_voice, dict):
            with open("media/guide/" + guidance + ".mp3", "wb") as f:
                f.write(guide_voice)

        new_guide = guide(
            right_answer=right,
            wrong_answer=wrong,
            tips="media/voice/" + guidance + ".mp3"
        )
        new_guide.save()
    username = request.session['username']
    classid = request.session['classid']

    return render(request, 'upload/upload_guide.html', {'username': username, 'classid': classid})
