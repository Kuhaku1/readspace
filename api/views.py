from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tool.redistool import redislinktool
import datetime
import time

from mainsite.models import Book
from mainsite.models import Author
from mainsite.models import Family
from mainsite.models import Press

from userspace.models import User
from userspace.models import Userbalance
from userspace.models import Usergrade
from userspace.models import Userhistroy
from userspace.models import Usercollection
from userspace.models import Usermessage
from userspace.models import Userreadtime
from userspace.models import Usercomment
# Create your views here.


@csrf_exempt
def sign_in_handle(request):
    context = {}
    usersession = request.session.get('userloginok')
    usersign = redislinktool.hgetall(usersession)
    if not usersign:
        # 以冗余降低服务器代价下面4行
        nowtime = datetime.datetime.now()
        extime = nowtime + datetime.timedelta(1)
        extime = extime.replace(hour=0, minute=0, second=0, microsecond=0)
        timedifference = extime - nowtime
        redislinktool.hmset(usersession, {'sign': 1, 'timeflag': str(
            int(time.mktime(extime.timetuple())))})
        redislinktool.expire(usersession, timedifference.seconds + 86400)
        context['state'] = 'ok'
        context['sign'] = '1'
        result = JsonResponse(context)
    else:
        if int(time.time()) - int(usersign[b'timeflag'].decode()) > 0:
            nowtime = datetime.datetime.now()
            extime = nowtime + datetime.timedelta(1)
            extime = extime.replace(hour=0, minute=0, second=0, microsecond=0)
            timedifference = extime - nowtime
            sign = int(usersign[b'sign'].decode()) + 1
            redislinktool.hmset(usersession, {'sign': sign, 'timeflag': str(
                int(time.mktime(extime.timetuple())))})
            if sign != 7:
                redislinktool.expire(
                    usersession, timedifference.seconds + 86400)
            else:
                redislinktool.expire(usersession, timedifference.seconds)
            context['state'] = 'ok'
            context['sign'] = str(sign)
        else:
            context['state'] = 'stop'
            context['sign'] = '0'
        result = JsonResponse(context)
    return result


@csrf_exempt
def find_book_from_screen(request):
    v1 = request.POST.get("v1")
    family = request.POST.get("family", "奇幻")
    state = request.POST.get("state", "已完结")

    if family == "全部" and state == "全部":
        book = Book.userManager.order_by('id')[0:18]
    elif family == "全部":
        book = Book.userManager.filter(
            state=state).order_by('-collection')[0:18]
    elif state == "全部":
        book = list()
        name = ""
        for qwer in Family.family_choices:
            if qwer[1] == family:
                name = qwer[0]
        familys = Family.userManager.filter(name=name)[0:18]
        for tmp in familys:
            book.append(tmp.book)
    else:
        book = list()
        name = ""
        for qwer in Family.family_choices:
            if qwer[1] == family:
                name = qwer[0]
        familys = Family.userManager.filter(name=name)[0:18]

        dbstate = ''
        for qwer in Book.classify_choices:
            if qwer[1] == state:
                dbstate = qwer[0]
        for tmp in familys:
            if tmp.book.state == dbstate:
                book.append(tmp.book)
    result = {
        "result": [],
    }

    for tmp in book:
        itme = dict()
        itme['idurl'] = reverse('mainsite:book', args=(tmp.id,))
        itme['name'] = tmp.name
        itme['image'] = tmp.image.url
        itme['lastUpdated'] = tmp.lastUpdated
        result['result'].append(itme)
    return JsonResponse(result)
    # Family.userManager.filter(pk=bookid).first()


def search_book_from_search_view(request):
    bookname = request.GET.get("bn")
    print(bookname)
    book = Book.userManager.filter(name__icontains=bookname).all()
    bookresult = list()
    for tmp in book:
        bookitem = dict()
        bookitem['id'] = tmp.id
        bookitem['name'] = tmp.name
        bookitem['state'] = tmp.state
        bookitem['image'] = tmp.image.url
        bookitem['profiles'] = tmp.profiles
        bookitem['lastUpdated'] = tmp.lastUpdated
        bookitem['publicatioDay'] = tmp.publicatioDay
        bookitem['publishers'] = tmp.publishers.id
        bookitem['statedis'] = tmp.get_state_display()
        bookresult.append(bookitem)
    result = dict()
    result['result'] = bookresult
    return JsonResponse(result)


def booklike_view(request):
    bookid = request.POST.get("bookid")
    event = request.POST.get("event")
    username = request.session.get('userloginok')
    if not bookid or not event or not username:
        result = dict()
        result['state'] = "error"
        result['reason'] = "参数错误"
        return JsonResponse(result)
    book = Book.userManager.filter(id=bookid).first()
    user = User.userManager.filter(username=username).first()
    if book and user:
        like = Usercollection.UserLikesManager.filter(
            user=user, book=book).first()
        if like:
            if event == "ok":
                result = dict()
                result['result'] = "重复"
                result['state'] = "ok"
                return JsonResponse(result)
            elif event == "cancel":
                print("删除")
                like.delete()
                result = dict()
                result['result'] = "成功取消点赞"
                result['state'] = "ok"
                return JsonResponse(result)
            else:
                result = dict()
                result['reason'] = "event参数错误"
                result['state'] = "error"
                return JsonResponse(result)
        else:
            if event == "ok":
                print("创建")
                nowtime = datetime.datetime.now()
                newlike = Usercollection(
                    user=user, book=book, collectiontime=nowtime, event=Usercollection.likes)
                newlike.save()
                result = dict()
                result['result'] = "成功点赞"
                result['state'] = "ok"
                return JsonResponse(result)
            elif event == "cancel":
                result = dict()
                result['result'] = "空操作"
                result['state'] = "ok"
                return JsonResponse(result)
            else:
                result = dict()
                result['reason'] = "event参数错误"
                result['state'] = "error"
                return JsonResponse(result)
    else:
        result = dict()
        result['state'] = "error"
        result['reason'] = "用户或图书不存在"
        return JsonResponse(result)


def bookcollection_view(request):
    bookid = request.POST.get("bookid")
    event = request.POST.get("event")
    username = request.session.get('userloginok')
    if not bookid or not event or not username:
        result = dict()
        result['state'] = "error"
        result['reason'] = "参数错误"
        return JsonResponse(result)
    book = Book.userManager.filter(id=bookid).first()
    user = User.userManager.filter(username=username).first()
    if book and user:
        collection = Usercollection.UserCollectionManager.filter(
            user=user, book=book).first()
        if collection:
            if event == "ok":
                result = dict()
                result['result'] = "重复"
                result['state'] = "ok"
                return JsonResponse(result)
            elif event == "cancel":
                print("删除")
                collection.delete()
                result = dict()
                result['result'] = "成功取消收藏"
                result['state'] = "ok"
                return JsonResponse(result)
            else:
                result = dict()
                result['reason'] = "event参数错误"
                result['state'] = "error"
                return JsonResponse(result)
        else:
            if event == "ok":
                print("创建")
                nowtime = datetime.datetime.now()
                newcollection = Usercollection(
                    user=user, book=book, collectiontime=nowtime, event=Usercollection.collection)
                newcollection.save()
                result = dict()
                result['result'] = "成功收藏"
                result['state'] = "ok"
                return JsonResponse(result)
            elif event == "cancel":
                result = dict()
                result['result'] = "空操作"
                result['state'] = "ok"
                return JsonResponse(result)
            else:
                result = dict()
                result['reason'] = "event参数错误"
                result['state'] = "error"
                return JsonResponse(result)
    else:
        result = dict()
        result['state'] = "error"
        result['reason'] = "用户或图书不存在"
        return JsonResponse(result)


def bookcoin_view(request):
    bookid = request.POST.get("bookid")
    event = request.POST.get("event")
    username = request.session.get('userloginok')
    if not bookid or not event or not username:
        result = dict()
        result['state'] = "error"
        result['reason'] = "参数错误"
        return JsonResponse(result)
    book = Book.userManager.filter(id=bookid).first()
    user = User.userManager.filter(username=username).first()
    if book and user:
        coin = Usercollection.UserCoinManager.filter(
            user=user, book=book).first()
        if coin:
            if event == "ok":
                result = dict()
                result['result'] = "重复"
                result['state'] = "ok"
                return JsonResponse(result)
            else:
                result = dict()
                result['reason'] = "event参数错误"
                result['state'] = "error"
                return JsonResponse(result)
        else:
            if event == "ok":
                print("创建")
                nowtime = datetime.datetime.now()
                newcollection = Usercollection(
                    user=user, book=book, collectiontime=nowtime, event=Usercollection.coin)
                newcollection.save()
                result = dict()
                result['result'] = "成功投币"
                result['state'] = "ok"
                return JsonResponse(result)
            else:
                result = dict()
                result['reason'] = "event参数错误"
                result['state'] = "error"
                return JsonResponse(result)
    else:
        result = dict()
        result['state'] = "error"
        result['reason'] = "用户或图书不存在"
        return JsonResponse(result)


# Userreadtime
@csrf_exempt
def readtimehandle(request):
    """
    # 大bug 这个接口可以被调用
    用户阅读时间管理
    """
    bookid = request.POST.get("bookid")
    event = request.POST.get("event")
    username = request.session.get('userloginok')
    # username = "lixingyu"
    if username:
        # user sumtime lasttime
        user = User.userManager.filter(username=username).first()
        usertime = Userreadtime.object.filter(user=user).first()
        if usertime:
            pass
            nowtime = int(time.time())
            oldtime = usertime.lasttime
            # usertime.lasttime = nowtime
            if nowtime-oldtime >= 5:
                usertime.lasttime = nowtime
                usertime.sumtime = usertime.sumtime + 5
                usertime.save()
                result = dict()
                result['state'] = "ok"
                return JsonResponse(result)
            else:
                result = dict()
                result['reason'] = "请以5s为周期发起请求"
                result['state'] = "ok"
                return JsonResponse(result)
        else:
            nowtime = int(time.time())
            usertime = Userreadtime(user=user, sumtime=0, lasttime=nowtime)
            usertime.save()
            result = dict()
            result['state'] = "ok"
            return JsonResponse(result)
    else:
        result = dict()
        result['state'] = "error"
        result['reason'] = "3275605460@qq.com"
        return JsonResponse(result)


def view_user_submit_comment(request):
    bookid = request.POST.get("bookid")
    username = request.session.get('userloginok')
    message = request.POST.get("message")
    book = Book.userManager.filter(id=bookid).first()
    if username and message and book:
        user = User.userManager.filter(username=username).first()
        nowtime = datetime.datetime.now()
        newcomment = Usercomment(
            user=user, book=book, commenttime=nowtime, comment=message)
        newcomment.save()
        result = dict()
        result['state'] = "ok"
        return JsonResponse(result)
    else:
        result = dict()
        result['state'] = "error"
        result['reason'] = "3275605460@qq.com"
        return JsonResponse(result)
