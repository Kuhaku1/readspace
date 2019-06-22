from django.http import HttpResponseRedirect
from django.urls import reverse


def is_login(request):
    username = request.session.get('userloginok')
    if username:
        return username
    else:
        return False


def login_verification(func):
    """需要登陆验证"""

    def wapper(*args, **kwargs):
        if not args[0].session.get('userloginok'):
            resp = HttpResponseRedirect(reverse('userspace:login'))
            resp.set_cookie(key='fromlogin', value=args[0].path)
            return resp
        else:
            return func(*args, **kwargs)

    return wapper
