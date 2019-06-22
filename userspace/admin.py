
from django.contrib import admin

from .models import User
from .models import Userbalance
from .models import Usergrade
from .models import Userhistroy
from .models import Usercollection
from .models import Usermessage
from .models import Userreadtime
from .models import Usercomment


class UserbalanceInline(admin.StackedInline):
    model = Userbalance
    extra = 1


class UsergradeInline(admin.StackedInline):
    model = Usergrade
    extra = 1


class UserAdmin(admin.ModelAdmin):
    # 可以显示的字段
    list_display = ('id', 'username', 'password', 'name',
                    'address', 'contact', "mailbox", "profiles", 'is_Delete')
    # 依据以下选项搜索
    search_fields = ('username', 'name')

    inlines = [UserbalanceInline, UsergradeInline]
    # 依据以下选项过滤
    # list_filter = ('publishers',)
    # 日期过滤***********
    # date_hierarchy = 'publicatioDay'
    # 排序
    # ordering = ('id',)
    # fields=('','','','','','','')
    # 将添加元素时外键位变成文本框加选择，而不是以前下拉框
    # raw_id_fields = ('publishers',)
    fields = ('username', 'password', 'name',
              'address', 'contact', "mailbox", "profiles", 'is_Delete')


admin.site.register(User, UserAdmin)


class UserbalanceAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)
    list_display = ('id', 'user', 'money', 'coin', 'is_vip', 'expirationdate')
    raw_id_fields = ('user',)


admin.site.register(Userbalance, UserbalanceAdmin)


class UsergradeAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)
    list_display = ('id', 'user', 'grade', 'readtime', 'experience')
    raw_id_fields = ('user',)


admin.site.register(Usergrade, UsergradeAdmin)


class UserhistroyAdmin(admin.ModelAdmin):
    search_fields = ('user__username', "book__name")
    list_display = ('id', 'user', 'book', 'subsection', 'lastUpdated')
    date_hierarchy = 'lastUpdated'
    raw_id_fields = ('user', "book", "subsection")


admin.site.register(Userhistroy, UserhistroyAdmin)


class UsercollectionAdmin(admin.ModelAdmin):
    search_fields = ('user__username', "book__name")
    list_display = ('id', 'user', 'book', 'collectiontime', 'event')
    date_hierarchy = 'collectiontime'
    raw_id_fields = ('user', "book")


admin.site.register(Usercollection, UsercollectionAdmin)


class UsermessageAdmin(admin.ModelAdmin):
    search_fields = ('fromuser__username', "touser__username")
    list_display = ('id', 'fromuser',
                    'touser', 'message', 'messagetime', "is_Delete", "is_views")
    date_hierarchy = 'messagetime'
    raw_id_fields = ('fromuser', "touser")


admin.site.register(Usermessage, UsermessageAdmin)


class UserreadtimeAdmin(admin.ModelAdmin):
    search_fields = ("user__username",)
    list_display = ('id', 'user', 'sumtime', 'lasttime')


admin.site.register(Userreadtime, UserreadtimeAdmin)


class UsercommentAdmin(admin.ModelAdmin):
    search_fields = ("user__username",)
    list_display = ('id', 'user', 'book', 'comment',
                    'commenttime', 'is_Delete')


admin.site.register(Usercomment, UsercommentAdmin)
