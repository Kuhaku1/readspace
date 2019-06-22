from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mainsite.models import Book, BookRanking
from tool.redistool import redislinktool
from tool.login import login_verification
import datetime
import time


from .models import User
from .models import Userbalance
from .models import Usergrade
from .models import Userhistroy
from .models import Usercollection
from .models import Usermessage


def login(request):
    context = {}
    context['username'] = request.COOKIES.get('username', "")
    context['user_error'] = False
    return render(request, 'userspace/login.html', context)


def loginhandle(request):
    data = request.POST
    if not data:
        return HttpResponseRedirect(reverse('userspace:login'))
    else:
        try:
            if 'username' in data and 'userpassword' in data:
                user = User.userManager.filter(
                    username=data['username']).first()
                if user:
                    if user.password == data['userpassword']:

                        request.session['userloginok'] = data['username']
                        request.session.set_expiry(0)
                        loginpath = request.COOKIES.get('fromlogin')
                        if loginpath:
                            httpres = HttpResponseRedirect(loginpath)
                            httpres.delete_cookie('fromlogin')
                            if 'usercheck' in data:
                                if data['usercheck'] == 'on':
                                    httpres.set_cookie(
                                        key='username', value=data['username'], expires=datetime.datetime.now()+datetime.timedelta(days=14))
                                else:
                                    httpres.delete_cookie('username')
                            return httpres
                        else:
                            httpres = HttpResponseRedirect('/')
                            if 'usercheck' in data:
                                if data['usercheck'] == 'on':
                                    httpres.set_cookie(
                                        key='username', value=data['username'], expires=datetime.datetime.now()+datetime.timedelta(days=14))
                                else:
                                    httpres.delete_cookie('username')
                            return httpres
                context = dict()
                context["username"] = ""
                if 'usercheck' in data:
                    if data['usercheck'] == 'on':
                        context["username"] = data['username']
                context['user_error'] = True
                return render(request, 'userspace/login.html', context)
                # password
                # usercheck
            else:
                return render(request, 'userspace/login.html')
        except Exception as e:
            print("ddd")
            context = {'user_error': True}
            return render(request, 'userspace/login.html', context)


@login_verification
def sign_in(request):
    usersession = request.session.get('userloginok')
    usersign = redislinktool.hgetall(usersession)
    context = dict()
    if usersign:
        if int(time.time()) - int(usersign[b'timeflag'].decode()) > 0:
            context['flag'] = True
            context['sign'] = int(usersign[b'sign'].decode())+1
        else:
            context['flag'] = False
            context['sign'] = int(usersign[b'sign'].decode())
    else:
        context['flag'] = True
        context['sign'] = 1
    return render(request, 'userspace/sign_in.html', context)


@login_verification
def home(request):
    print(request.session.session_key)
    username = request.session.get('userloginok')
    user = User.userManager.filter(username=username).first()
    context = dict()
    context["user"] = user
    return render(request, 'userspace/home.html', context)


@login_verification
def message(request):
    username = request.session.get('userloginok')
    user = User.userManager.filter(username=username).first()
    messages = Usermessage.userManager.filter(touser=user).all()
    context = dict()
    context["message"] = messages
    return render(request, "userspace/message.html", context)


@login_verification
def collection(request):
    username = request.session.get('userloginok')
    user = User.userManager.filter(username=username).first()
    collections = Usercollection.UserCollectionManager.filter(user=user).all()
    context = dict()
    context["collections"] = collections
    return render(request, "userspace/collection.html", context)


@login_verification
def histroy(request):
    username = request.session.get('userloginok')
    user = User.userManager.filter(username=username).first()
    userhistroy = Userhistroy.object.filter(
        user=user).order_by("-lastUpdated").all()
    context = dict()
    context['userhistroy'] = userhistroy
    return render(request, "userspace/histroy.html", context)


@login_verification
def balance(request):
    username = request.session.get('userloginok')
    user = User.userManager.filter(username=username).first()
    userbalance = Userbalance.object.filter(user=user).first()
    context = dict()
    context['userbalance'] = userbalance
    return render(request, "userspace/balance.html", context)


def useractivityspace(request):
    return render(request, "userspace/useractivityspace.html")


@login_verification
def userdetails(request):
    username = request.session.get('userloginok')
    user = User.userManager.filter(username=username).first()
    context = dict()
    context['user'] = user
    return render(request, "userspace/userdetails.html", context)


#      冗余函数
#      冗余函数
#      冗余函数
#      冗余函数
#      冗余函数
#      冗余函数
#      冗余函数
#      冗余函数
#      冗余函数
#      冗余函数
#      冗余函数
#      冗余函数
#      冗余函数
#      冗余函数


def clearsession(request):
    request.session.clear()
    return HttpResponse('ok')


def clear_book_rank(request):
    booklist = Book.object.all()
    for booktmp in booklist:
        bookranktmp = booktmp.bookranking
        if bookranktmp:
            bookranktmp.popularity = 0
            bookranktmp.scoreValue = 0
            bookranktmp.scoreNumber = 0
            bookranktmp.collection = 0
            bookranktmp.save()
        # BookRanking.userManager.createranking(booktmp)
    return HttpResponse('ok')


def createuser(request):
    User.userManager.create_user("lixingyuuser", "lixingyupwd", "lixingyuname")
    return HttpResponse("ok")
