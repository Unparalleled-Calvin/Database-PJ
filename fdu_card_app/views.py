from django.shortcuts import render, HttpResponse
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
        return render(request, "login.html")

def user(request):
    return render(request, "user.html")
    
def canteen(request):
    if request.method == 'POST':
        ret_dict = {}
        ret_dict['ret'] = 1
        ret = JsonResponse(ret_dict)
        return ret
    else:
        return render(request, "canteen.html")