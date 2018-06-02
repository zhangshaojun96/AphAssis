from django.contrib.auth import authenticate
import json
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template.loader import get_template

from login.models import register

user_id = -1
Login_user = ''

 #if(user_id == -1):
    #	login_user = ''
        #user = list(register.objects.filter(id = user_id))
        #data = user.res_username


def after_login(request):
	global Login_user
	return# render(request,'index',{'username':Login_user})

def login(request):
	global Login_user
	if request.method == 'POST':
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		m = register.objects.filter(res_username=username, res_password=password)
		if m:
			#user_id = m.id
			Login_user = username
			resp = {'status':'success' , 'reason': '登录成功'}
			return HttpResponse(json.dumps(resp), content_type="application/json")
		else:
			user_id = -1
			resp = {'status': 'failed', 'reason': '用户名或密码错误'}
			return HttpResponse(json.dumps(resp), content_type="application/json")
	return render(request, 'login/login.html')


def nregister(request):
	if request.method == 'POST':
		res_username = request.POST.get('res_username', None)
		res_password = request.POST.get('res_password', None)
		res_email = request.POST.get('res_email', None)
		res_id= request.POST.get('res_type', None)
		age = request.POST.get('age', None)
		profession = request.POST.get('profession', None)
		education = request.POST.get('education', None)
		print( education)
		a = register.objects.filter(Q(res_username=res_username))
		flag = 0
		for e in a:
			flag = 1
			break
		if (flag == 1):
			resp = {'status':'failed' , 'reason': '用户名重复'}
			return HttpResponse(json.dumps(resp), content_type="application/json")
		else:
			new_register = register(
				res_username=res_username,
				res_password=res_password,
				res_email=res_email,
				res_id=res_type,
				age=age,
				profession=profession,
				education=education
			)
			new_register.save()
			resp = {'status': 'success', 'reason': '注册成功'}
			return HttpResponse(json.dumps(resp), content_type="application/json")
	return render(request, 'login/register.html')
