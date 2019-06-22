from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from mainsite.models import Subsection
from userspace.models import User, Userbalance


def have_permission_to_read(func):

    def wapper(*args, **kwargs):
        sid = kwargs.get("sid")
        request = args[0]
        subsection = Subsection.userManager.filter(
            pk=sid).first()
    # print(subsection)
        if not subsection:
            return HttpResponseRedirect(reverse('mainsite:index'))
        else:
            username = request.session.get('userloginok')
            if username:
                user = User.userManager.filter(username=username).first()
                userbalance = Userbalance.object.filter(user=user).first()
                if userbalance.is_vip:
                    return func(*args, **kwargs)
                else:
                    pirce = subsection.price
                    discount = subsection.discount
                    if pirce*discount <= 0:
                        return func(*args, **kwargs)
                    else:
                        return HttpResponse("该章节收费")
            else:
                return HttpResponseRedirect(reverse('mainsite:index'))

    return wapper
