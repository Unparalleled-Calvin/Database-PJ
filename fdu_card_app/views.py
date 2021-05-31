from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.db import connection
from datetime import datetime, timedelta
import sys
import json
import re
sys.path.append('.\\fdu_card_app')
from methods import analyse
from methods import select
from methods import insert
from methods import update
from methods import delete
cursor = connection.cursor()

login_info = dict()
kick_out = set()

# automatic backup
import os
from datetime import datetime
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
def backup():    
    os.system("pg_dump -a \"host=127.0.0.1 hostaddr=127.0.0.1 port=5432 user=postgres password=admin dbname=dbpj\" > backup.sql")
scheduler = BackgroundScheduler()
scheduler.add_job(backup, 'cron', hour='0', minute='0', args=[])
scheduler.start()

# Create your views here.
def getIP(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        return request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        return request.META.get("REMOTE_ADDR")

def kickout(request, ip):
    response = render(request, "login.html", {'kickout':1})
    response.delete_cookie('ID')
    kick_out.discard(ip)
    return response

def login(request):
    ip = getIP(request)
    if ip in kick_out:
        return kickout(request, ip)
    if request.method == 'POST':
        ret_dict = {}
        if(select.check_identity(cursor, request.POST['ID'], request.POST['passwd'])):
            ret_dict['ret'] = 1
            ret = JsonResponse(ret_dict)
            ret.set_cookie(
                'ID', request.POST['ID'], expires=datetime.now() + timedelta(minutes=5))
            if request.POST['ID'] in login_info and login_info[request.POST['ID']] != ip:
                kick_out.add(login_info[request.POST['ID']])
            login_info[request.POST['ID']] = ip
        else:
            ret_dict['ret'] = 2
            ret = JsonResponse(ret_dict)
        return ret
    else:
        if 'ID' in request.COOKIES:
            return HttpResponseRedirect('/user')
        else:
            return render(request, "login.html", {'kickout':0})


def logout(request):
    response = HttpResponseRedirect('/login')
    if 'ID' in request.COOKIES:
        response.delete_cookie('ID')
        login_info.pop(request.COOKIES['ID'])
    return response


def register(request):
    ip = getIP(request)
    if ip in kick_out:
        return kickout(request, ip)
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
    if request.COOKIES['ID'] != 'admin':
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        if request.POST['name'] == '' or request.POST['ID'] == '':
            ret_dict['ret'] = 2
            ret_dict['msg'] = '学工号和姓名不能为空'
        elif ID_invalid(request.POST):
            ret_dict['ret'] = 2
        elif request.POST['identity'] == 'student' and request.POST['enrolmentdt'] == '':
            ret_dict['ret'] = 2
            ret_dict['msg'] = '入学时间不能为空'
        elif request.POST['identity'] == 'student' and request.POST['stuclass'] == '':
            ret_dict['ret'] = 2
            ret_dict['msg'] = '班级不能为空'
        elif request.POST['identity'] == 'student' and request.POST['dormitory'] == '':
            ret_dict['ret'] = 2
            ret_dict['msg'] = '寝室楼不能为空'
        elif request.POST['identity'] == 'student' and select.verify_dormitory(cursor, request.POST['dormitory']) == 0:
            ret_dict['ret'] = 2
            ret_dict['msg'] = '寝室楼不存在'
        elif request.POST['identity'] == 'teacher' and request.POST['birth'] == '':
            ret_dict['ret'] = 2
            ret_dict['msg'] = '出生年月不能为空'
        elif request.POST['identity'] == 'others' and request.POST['work'] == '':
            ret_dict['ret'] = 2
            ret_dict['msg'] = '工作事由不能为空'
        else:
            ret_dict['ret'] = 1
            ret_dict['msg'] = '用户的初始密码为：000000'
        if ret_dict['ret'] == 1:
            try:
                insert.insert_person(
                    cursor, request.POST['ID'], request.POST['name'])
                if request.POST['identity'] == 'student':
                    insert.insert_card(
                        cursor, request.POST['ID'], request.POST['dormitory'])
                    insert.insert_student(
                        cursor, request.POST['ID'], request.POST['enrolmentdt'], request.POST['stuclass'])
                elif request.POST['identity'] == 'teacher':
                    insert.insert_card(cursor, request.POST['ID'])
                    insert.insert_teacher(
                        cursor, request.POST['ID'], request.POST['birth'], request.POST['rank'])
                elif request.POST['identity'] == 'others':
                    insert.insert_card(cursor, request.POST['ID'])
                    insert.insert_others(
                        cursor, request.POST['ID'], request.POST['work'])
            except Exception:
                connection.rollback()
                ret_dict['ret'] = 2
                ret_dict['msg'] = '插入失败，该用户已存在'
            else:
                connection.commit()
        ret = JsonResponse(ret_dict)
        return ret
    else:
        data = select.select_information(
            cursor, request.COOKIES['ID'])[2][0][0]
        data['name'] = "\"" + \
            select.select_v_name(cursor, request.COOKIES['ID']) + "\""
        return render(request, "register.html", data)


def user(request):
    ip = getIP(request)
    if ip in kick_out:
        return kickout(request, ip)

    def toDataDict(dataTuple, forChange=None):  # 将元组数据转成字典数据，并将其中的时间类转成字符串
        data_dict = {}
        data_dict["heads"] = dataTuple[0]
        data_dict["dataKeys"] = dataTuple[1]
        data_dict["data"] = dataTuple[2]
        if forChange != None:
            for i in data_dict["data"][0]:
                i[forChange] = str(i[forChange])
        return data_dict

    if 'ID' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    else:
        if request.method == 'POST':
            ret_dict = {}
            if request.COOKIES['ID'] != 'admin':
                try:
                    if request.POST['role'] == 'charge':
                        ret_dict["remainingsum"] = str(update.update_remainingsum(
                            cursor, request.COOKIES['ID'], request.POST['amount']))
                    elif request.POST['role'] == 'passwd':
                        ret_dict['data'] = int(update.update_passwd(
                            cursor, request.COOKIES['ID'], request.POST['new_passwd']))
                    elif request.POST['role'] == 'update':
                        ret_dict['data'] = int(update.update_card(
                            cursor, request.COOKIES['ID'], request.POST['new_passwd']))
                    elif request.POST['method'] == "select":
                        if request.POST['role'] == 'record':
                            ret_dict['data'] = toDataDict(select.select_v_record(
                                cursor, request.COOKIES['ID'], request.POST['start'], request.POST['end']), 'recordtm')
                        elif request.POST['role'] == 'access':
                            ret_dict['data'] = toDataDict(select.select_v_access(
                                cursor, request.COOKIES['ID'], request.POST['start'], request.POST['end']), 'accesstm')
                        elif request.POST['role'] == 'consume':
                            ret_dict['data'] = toDataDict(select.select_v_consume(
                                cursor, request.COOKIES['ID'], request.POST['start'], request.POST['end']), 'consumetm')
                    ret_dict['ret'] = 1
                except Exception:
                    ret_dict['ret'] = 0
            else:
                try:
                    if request.POST['method'] == 'select':
                        if request.POST['role'] == 'student':
                            ret_dict['data'] = toDataDict(
                                select.select_student(cursor), "enrolmentdt")
                        elif request.POST['role'] == 'teacher':
                            ret_dict['data'] = toDataDict(
                                select.select_teacher(cursor), "birthday")
                        elif request.POST['role'] == 'others':
                            ret_dict['data'] = toDataDict(
                                select.select_others(cursor))
                        elif request.POST['role'] == 'record_all':
                            ret_dict['data'] = toDataDict(select.select_record(
                                cursor, request.POST['start'], request.POST['end']))
                        elif request.POST['role'] == 'access_all':
                            ret_dict['data'] = toDataDict(select.select_access(
                                cursor, request.POST['start'], request.POST['end']), "accesstm")
                        elif request.POST['role'] == 'consume_all':
                            ret_dict['data'] = toDataDict(select.select_consume(
                                cursor, request.POST['start'], request.POST['end']))
                    if request.POST['method'] == "update":
                        if request.POST['role'] == "passwd":
                            ret_dict['data'] = int(
                                update.default_passwd(cursor, request.POST['ID']))
                        elif request.POST['role'] == "valid1":
                            ret_dict['data'] = int(
                                update.update_valid1(cursor, request.POST['ID']))
                        elif request.POST['role'] == "valid2":
                            ret_dict['data'] = int(
                                update.update_valid2(cursor, request.POST['ID']))
                        elif request.POST['role'] == "cdno":
                            ret_dict['data'] = int(update.update_cdno(
                                cursor, request.POST['ID'], request.POST['info']))
                        elif request.POST['role'] == "class":
                            ret_dict['data'] = int(update.update_class(
                                cursor, request.POST['ID'], request.POST['info']))
                        elif request.POST['role'] == "rank":
                            ret_dict['data'] = int(update.update_rank(
                                cursor, request.POST['ID'], request.POST['rank']))
                        elif request.POST['role'] == "work":
                            ret_dict['data'] = int(update.update_work(
                                cursor, request.POST['ID'], request.POST['info']))
                        elif request.POST['role'] == "delete_person":
                            ret_dict['data'] = int(
                                delete.delete_person(cursor, request.POST['ID']))
                    ret_dict['ret'] = 1
                except Exception:
                    ret_dict['ret'] = 0
            return JsonResponse(ret_dict)
        else:
            data = select.select_information(
                cursor, request.COOKIES['ID'])[2][0][0]
            data['name'] = "\"" + \
                select.select_v_name(cursor, request.COOKIES['ID']) + "\""
            data['data'] = toDataDict(
                select.select_student(cursor), "enrolmentdt")
            data['today_consume'] = select.select_amount(
                cursor, request.COOKIES['ID'])
            return render(request, "user.html" if request.COOKIES['ID'] != 'admin' else 'admin.html', data)


def canteen(request):
    ip = getIP(request)
    if ip in kick_out:
        return kickout(request, ip)
    if 'ID' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    elif request.method == 'POST':
        ret_dict = {}
        if request.COOKIES['ID'] != 'admin':
            ret_dict['ret'] = int(insert.insert_consume(
                cursor, request.POST['wno'], request.COOKIES['ID'], request.POST['cuisineid'], request.POST['amount']))
        else:
            try:
                if request.POST['method'] == 'update':
                    ret_dict['ret'] = int(update.update_canteen(
                        cursor, request.POST['wno'], request.POST['wname'], request.POST['wadmin'], request.POST['wtel']))
                elif request.POST['method'] == 'delete':
                    ret_dict['ret'] = int(delete.delete_canteen(
                        cursor, request.POST['wno']))
                elif request.POST['method'] == 'insert':
                    ret_dict['ret'] = int(insert.insert_canteen(
                        cursor, request.POST['wno'], request.POST['wname'], request.POST['wadmin'], request.POST['wtel']))
            except Exception:
                ret_dict['ret'] = 0
        ret = JsonResponse(ret_dict)
        return ret

    else:
        return render(request, "canteen.html",  {
            'canteen': json.dumps({'canteen': select.select_canteen(cursor)[2][0]}),
            'name': "\"" + select.select_v_name(cursor, request.COOKIES['ID']) + "\""
        })


def leave(request):
    ip = getIP(request)
    if ip in kick_out:
        return kickout(request, ip)
    if 'ID' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    elif request.method == 'POST':
        ret_dict = {}
        if request.COOKIES['ID'] != 'admin':
            ret_dict['ret'] = int(insert.insert_record(
                cursor, request.COOKIES['ID'], request.POST['gno'], request.POST['inout']))
        else:
            try:
                if request.POST['method'] == 'update':
                    ret_dict['ret'] = int(update.update_gate(
                        cursor, request.POST['gno'], request.POST['gname'], request.POST['gadmin'], request.POST['gtel']))
                elif request.POST['method'] == 'delete':
                    ret_dict['ret'] = int(delete.delete_gate(
                        cursor, request.POST['gno']))
                elif request.POST['method'] == 'insert':
                    ret_dict['ret'] = int(insert.insert_gate(
                        cursor, request.POST['gno'], request.POST['gname'], request.POST['gadmin'], request.POST['gtel']))
            except Exception:
                ret_dict['ret'] = 0
        ret = JsonResponse(ret_dict)
        return ret
    else:
        gList = select.select_gate(cursor)[2][0]
        return render(request, "leave.html",  {
            'gate': json.dumps({'gList': gList}),
            'name': "\"" + select.select_v_name(cursor, request.COOKIES['ID']) + "\""
        })


def access(request):
    ip = getIP(request)
    if ip in kick_out:
        return kickout(request, ip)
    if 'ID' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    elif request.method == 'POST':
        ret_dict = {}
        if request.COOKIES['ID'] != 'admin':
            ret_dict['ret'] = int(insert.insert_access(
                cursor, request.COOKIES['ID'], request.POST['dno']))
        else:
            try:
                if request.POST['method'] == 'update':
                    ret_dict['ret'] = int(update.update_dormitory(
                        cursor, request.POST['dno'], request.POST['dadmin'], request.POST['dtel'], request.POST['dfloor']))
                elif request.POST['method'] == 'delete':
                    ret_dict['ret'] = int(delete.delete_dormitory(
                        cursor, request.POST['dno']))
                elif request.POST['method'] == 'insert':
                    ret_dict['ret'] = int(insert.insert_dormitory(
                        cursor, request.POST['dno'], request.POST['dadmin'], request.POST['dtel'], request.POST['dfloor']))
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
            'dormitory': json.dumps({'dList': dList, "dnoList": dnoList}),
            'name': "\"" + select.select_v_name(cursor, request.COOKIES['ID']) + "\""
        })

def analysis(request):
    ip = getIP(request)
    if ip in kick_out:
        return kickout(request, ip)
    if 'ID' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    elif request.method == 'POST':
        ret_dict = {}
        if request.POST['role'] == 'record_count':
            analyse.select_record_times(cursor, request.POST['start'], request.POST['end'])
        elif request.POST['role'] == 'access_count':
            analyse.select_access_times(cursor, request.POST['start'], request.POST['end'])
        elif request.POST['role'] == 'profit':
            analyse.select_profit(cursor, request.POST['start'], request.POST['end'])
        elif request.POST['role'] == 'cuisine':
            analyse.select_cuisineid_times(cursor, request.POST['start'], request.POST['end'])
        elif request.POST['role'] == 'rank':
            analyse.select_rank_teacher(cursor, request.POST['start'], request.POST['end'])
        elif request.POST['role'] == 'class':
            analyse.select_class_student(cursor, request.POST['start'], request.POST['end'])
        elif request.POST['role'] == 'dormitory':
            analyse.select_dno_people(cursor, request.POST['start'], request.POST['end'])
        mode = re.compile(".*?(<div.+?></div>).*?<script>(.*?)</script>", re.DOTALL)
        try:
            with open(r"./graph.html", "r") as f:
                result = mode.findall(f.read())
                ret_dict['div'] = result[0][0]
                ret_dict['script'] = result[0][1]
            ret_dict['ret'] = 1
        except:
            ret_dict['ret'] = 0
        ret = JsonResponse(ret_dict)
        return ret
    else:
        return render(request, "analysis.html",  {
            'name': "\"" + select.select_v_name(cursor, request.COOKIES['ID']) + "\""
        })
