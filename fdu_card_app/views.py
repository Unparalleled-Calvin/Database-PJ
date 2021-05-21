from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect 
from django.http import JsonResponse
from django.db import connection
from datetime import datetime,timedelta
import sys
import json
sys.path.append('.\\fdu_card_app')
from methods import select
from methods import insert
from methods import update
from methods import delete
cursor = connection.cursor()

# Create your views here.        
def login(request):
    if request.method == 'POST':
        ret_dict = {}
        if(select.check_identity(cursor, request.POST['ID'], request.POST['passwd'])):
            ret_dict['ret'] = 1
            ret = JsonResponse(ret_dict)
            ret.set_cookie('ID', request.POST['ID'], expires = datetime.now() + timedelta(minutes = 5))
        else:
            ret_dict['ret'] = 2
            ret = JsonResponse(ret_dict)
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
        elif request.POST['identity'] == 'student' and request.POST['dormitory'] == '' :
            ret_dict['ret'] = 2
            ret_dict['msg'] = '寝室楼不能为空'
        elif request.POST['identity'] == 'teacher' and request.POST['birth'] == '':
            ret_dict['ret'] = 2
            ret_dict['msg'] = '出生年月不能为空'
        elif request.POST['identity'] == 'others' and request.POST['work'] == '' :
            ret_dict['ret'] = 2
            ret_dict['msg'] = '工作事由不能为空'
        else:
            ret_dict['ret'] = 1
            ret_dict['msg'] = '即将跳转至用户界面'
        if ret_dict['ret'] == 1:
            try:
                insert.insert_person(cursor, request.POST['ID'], request.POST['name'])
                if request.POST['identity'] == 'student':
                    insert.insert_card(cursor, request.POST['ID'], request.POST['dormitory'])
                    insert.insert_student(cursor, request.POST['ID'], request.POST['enrolmentdt'], request.POST['stuclass'])
                elif request.POST['identity'] == 'teacher':
                    insert.insert_card(cursor, request.POST['ID'])
                    insert.insert_teacher(cursor, request.POST['ID'], request.POST['birth'], request.POST['rank'])
                elif request.POST['identity'] == 'others':
                    insert.insert_card(cursor, request.POST['ID'])
                    insert.insert_others(cursor, request.POST['ID'], request.POST['work'])
            except Exception:
                connection.rollback()
                ret_dict['ret'] = 2
                ret_dict['msg'] = '插入失败，该用户已存在'
            else:
                connection.commit()
        ret = JsonResponse(ret_dict)
        ret.set_cookie('ID', request.POST['ID'], expires = datetime.now() + timedelta(minutes = 5))
        return ret
    else:
        return render(request, "register.html")

def reset(request):
    if request.method == 'POST':
        ret_dict = {}
        if request.POST['passwd'] == '' or request.POST['repasswd'] == '' or request.POST['ID'] == '' :
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
        if request.method == 'POST':
            ret_dict = {}
            try:
                remainingsum = update.update_remainingsum(cursor, request.COOKIES['ID'], request.POST['amount'])
                ret_dict["remainingsum"] = str(remainingsum)
                ret_dict['ret'] = 1
            except Exception:
                ret_dict['ret'] = 0
            return JsonResponse(ret_dict)
        else:
            data = select.select_information(cursor, request.COOKIES['ID'])[2][0][0]
            data['name'] = "\"" + select.select_v_name(cursor, request.COOKIES['ID']) + "\""
            return render(request, "user.html", data)
    
def canteen(request):
    if 'ID' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    elif request.method == 'POST':
        ret_dict = {}
        if request.COOKIES['ID'] != 'admin':
            ret_dict['ret'] = int(insert.insert_consume(cursor, request.POST['wno'], request.COOKIES['ID'], request.POST['cuisineid'], request.POST['amount']))
        else:
            try:
                if request.POST['method'] == 'update':
                    ret_dict['ret'] = int(update.update_canteen(cursor, request.POST['wno'], request.POST['wname'], request.POST['wadmin'], request.POST['wtel']))
                elif request.POST['method'] == 'delete':
                    ret_dict['ret'] = int(delete.delete_canteen(cursor, request.POST['wno']))
                elif request.POST['method'] == 'insert':
                    ret_dict['ret'] = int(insert.insert_canteen(cursor, request.POST['wno'], request.POST['wname'], request.POST['wadmin'], request.POST['wtel']))
            except Exception:
                ret_dict['ret'] = 0
        ret = JsonResponse(ret_dict)
        return ret
        
    else:
        return render(request, "canteen.html",  {
            'canteen': json.dumps({'canteen':select.select_canteen(cursor)[2][0]}),
            'name': "\"" + select.select_v_name(cursor, request.COOKIES['ID']) + "\""
        })

def access(request):
    if 'ID' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    elif request.method == 'POST':
        ret_dict = {}
        if request.COOKIES['ID'] != 'admin':
            ret_dict['ret'] = int(insert.insert_access(cursor, request.COOKIES['ID'], request.POST['dno']))
        else:
            try:
                if request.POST['method'] == 'update':
                    ret_dict['ret'] = int(update.update_dormitory(cursor, request.POST['dno'], request.POST['dadmin'], request.POST['dtel'], request.POST['dfloor']))
                elif request.POST['method'] == 'delete':
                    ret_dict['ret'] = int(delete.delete_dormitory(cursor, request.POST['dno']))
                elif request.POST['method'] == 'insert':
                    ret_dict['ret'] = int(insert.insert_dormitory(cursor, request.POST['dno'], request.POST['dadmin'], request.POST['dtel'], request.POST['dfloor']))
            except Exception:
                ret_dict['ret'] = 0
        ret = JsonResponse(ret_dict)
        return ret
    else:
        dList = select.select_dormitory(cursor)[2][0]
        dnoList = []
        for each in dList:
            dnoList.append(each['dno'])
        dnoList.sort()
        return render(request, "access.html",  {
            'dormitory': json.dumps({'dList':dList, "dnoList":dnoList}),
            'name': "\"" + select.select_v_name(cursor, request.COOKIES['ID']) + "\""
        })