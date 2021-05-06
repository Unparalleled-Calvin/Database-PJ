from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect 
from django.http import JsonResponse
from django.db import connection
from datetime import datetime,timedelta
import sys
sys.path.append('.\\fdu_card_app')
from methods import select
from methods import insert

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
        if 'ID' in request.COOKIES:
            return HttpResponseRedirect('/user')
        else:
            return render(request, "login.html")

def logout(request):
    response = HttpResponseRedirect('/login')
    if 'ID' in request.COOKIES:
        response.delete_cookie('ID')
    return response

def register(request):
    ret_dict = {}
    def ID_invalid(post):
        if post['identity'] == 'student' and len(post['ID']) != 11:
            ret_dict['msg'] = '学生的学工号必须为11位'
        elif post['identity'] == 'teacher' and len(post['ID']) != 6:
            ret_dict['msg'] = '老师的学工号必须为6位'
        elif post['identity'] == 'others' and len(post['ID']) != 5:
            ret_dict['msg'] = '外来人员的学工号必须为5位'
        else:
            return False
        return True
            
    if request.method == 'POST':
        if request.POST['name'] == ''  or request.POST['ID'] == '' :
            ret_dict['ret'] = 2
            ret_dict['msg'] = '用户名和学工号不能为空'
        elif ID_invalid(request.POST):
            ret_dict['ret'] = 2
        elif request.POST['identity'] == 'student' and request.POST['enrolmentdt'] == '' :
            ret_dict['ret'] = 2
            ret_dict['msg'] = '入学时间不能为空'
        elif request.POST['identity'] == 'student' and request.POST['stuclass'] == '' :
            ret_dict['ret'] = 2
            ret_dict['msg'] = '班级不能为空'
        elif request.POST['identity'] == 'teacher' and request.POST['age'] == '':
            ret_dict['ret'] = 2
            ret_dict['msg'] = '年龄不能为空'
        elif request.POST['identity'] == 'others' and request.POST['work'] == '' :
            ret_dict['ret'] = 2
            ret_dict['msg'] = '工作事由'
        else:
            ret_dict['ret'] = 1
            ret_dict['msg'] = '即将跳转至用户界面'
        if ret_dict['ret'] == 1:
            try:
                insert.insert_person(cursor, request.POST['ID'], request.POST['name'])
                insert.insert_card(cursor, request.POST['ID'])
                if request.POST['identity'] == 'student':
                    insert.insert_student(cursor, request.POST['ID'], request.POST['enrolmentdt'], request.POST['stuclass'])
                elif request.POST['identity'] == 'teacher':
                    insert.insert_teacher(cursor, request.POST['ID'], request.POST['age'], request.POST['rank'])
                elif request.POST['identity'] == 'others':
                    insert.insert_others(cursor, request.POST['ID'], request.POST['work'])
            except Exception:
                connection.rollback()
                ret_dict['ret'] = 2
                ret_dict['msg'] = '插入失败，该用户已存在'
            else:
                connection.commit()
                
        ret = JsonResponse(ret_dict)
        ret.set_cookie('ID', request.POST['ID'], expires = datetime.now() + timedelta(minutes = 5))
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
        ret.set_cookie('ID', request.POST['ID'], expires = datetime.now() + timedelta(minutes = 5))
        return ret
    else:
        return render(request, "reset.html")

def user(request):
    if 'ID' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    else:
        return render(request, "user.html")
    
def canteen(request):
    if 'ID' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    elif request.method == 'POST':
        ret_dict = {}
        ret_dict['ret'] = 1
        ret = JsonResponse(ret_dict)
        return ret
    else:
        return render(request, "canteen.html")