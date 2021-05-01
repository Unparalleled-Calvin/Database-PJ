from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect 
from django.http import JsonResponse
from django.db import connection
from datetime import datetime,timedelta
import sys
sys.path.append('.\\fdu_card_app')
from methods import select

cursor = connection.cursor()

# Create your views here.        
def login(request):
    if request.method == 'POST':
        ret_dict = {}
        if(request.POST['email'] == 'admin@fudan.edu.cn' and request.POST['passwd'] == 'admin'):
            ret_dict['ret'] = 1
        else:
            ret_dict['ret'] = 2
        ret = JsonResponse(ret_dict)
        ret.set_cookie('name', 'admin', expires = datetime.now() + timedelta(minutes = 5))
        return ret
    else:
        if 'name' in request.COOKIES.keys():
            return HttpResponseRedirect('/user')
        else:
            return render(request, "login.html")

def logout(request):
    response = HttpResponseRedirect('/login')
    if 'name' in request.COOKIES.keys():
        response.delete_cookie('name')
    return response

def register(request):
    if request.method == 'POST':
        ret_dict = {}
        if request.POST['name'] == '' or request.POST['passwd'] == '' or request.POST['repasswd'] == '' or request.POST['email'].split('@')[0] == '' :
            ret_dict['ret'] = 2
            ret_dict['msg'] = '必填项均不能为空'
        elif request.POST['identity'] == 'student' and request.POST['enrolmentdt'] == '' :
            ret_dict['ret'] = 2
            ret_dict['msg'] = '入学时间不能为空'
        elif request.POST['identity'] == 'teacher' and request.POST['age'] == '':
            ret_dict['ret'] = 2
            ret_dict['msg'] = '年龄不能为空'
        elif request.POST['identity'] == 'others' and request.POST['work'] == '' :
            ret_dict['ret'] = 2
            ret_dict['msg'] = '工作事由'
        elif request.POST['passwd'] != request.POST['repasswd']:
            ret_dict['ret'] = 2
            ret_dict['msg'] = '两次密码填写不一致'
        else:
            ret_dict['ret'] = 1
            ret_dict['msg'] = '即将跳转至用户界面'
        ret = JsonResponse(ret_dict)
        ret.set_cookie('name', request.POST['name'], expires = datetime.now() + timedelta(minutes = 5))
        return ret
    else:
        return render(request, "register.html")

def reset(request):
    if request.method == 'POST':
        ret_dict = {}
        if request.POST['passwd'] == '' or request.POST['repasswd'] == '' or request.POST['email'].split('@')[0] == '' :
            ret_dict['ret'] = 2
            ret_dict['msg'] = '必填项均不能为空'
        elif request.POST['passwd'] != request.POST['repasswd']:
            ret_dict['ret'] = 2
            ret_dict['msg'] = '两次密码填写不一致'
        else:
            ret_dict['ret'] = 1
            ret_dict['msg'] = '即将跳转至用户界面'
        ret = JsonResponse(ret_dict)
        ret.set_cookie('name', 'temp', expires = datetime.now() + timedelta(minutes = 5))
        return ret
    else:
        return render(request, "reset.html")

def user(request):
    if 'name' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    else:
        return render(request, "user.html")
    
def canteen(request):
    if 'name' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    elif request.method == 'POST':
        ret_dict = {}
        ret_dict['ret'] = 1
        ret = JsonResponse(ret_dict)
        return ret
    else:
        return render(request, "canteen.html")