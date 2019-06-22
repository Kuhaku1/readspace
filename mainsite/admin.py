from django.contrib import admin
from .models import Press
from .models import Author
from .models import Family
from .models import Book
from .models import Subsection
from .models import BookRanking
from .models import ThisLightNovelIsTerrific
from userspace.models import Usercollection
from userspace.models import User
from userspace.models import Usermessage
from django.utils.safestring import mark_safe  # 允许不转译
from decimal import Decimal


class FamilyInline(admin.StackedInline):
    model = Family
    raw_id_fields = ("book",)
    extra = 1


class BookAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            BookRanking.userManager.createranking(obj)
        else:
            aa = BookRanking.object.filter(book=obj)
            if not aa:
                BookRanking.userManager.createranking(obj)

    def show_image(self, obj):
        strtmp = "<img src='{url}' alt='图像' width=50>".format(
            url=obj.image.url)
        return mark_safe(strtmp)

    show_image.short_description = '图像'
    # 可以显示的字段
    list_display = ('id', 'name', 'state', 'show_image',
                    'publishers', 'publicatioDay', 'is_Delete')
    # 在book表中添加Family这是反外键配置
    inlines = [FamilyInline, ]
    # 依据以下选项搜索
    search_fields = ('name', 'publishers__name')
    # 依据以下选项过滤
    list_filter = ('publishers',)
    # 日期过滤***********
    date_hierarchy = 'publicatioDay'
    # 排序
    ordering = ('id',)
    # fields=('','','','','','','')
    # 将添加元素时外键位变成文本框加选择，而不是以前下拉框
    raw_id_fields = ('publishers',)
    fields = ('name', 'state', 'publishers', 'publicatioDay',
              'image', 'profiles', 'lastUpdated', 'is_Delete')


admin.site.register(Book, BookAdmin)


class PressAdmin(admin.ModelAdmin):

    def set_profiles(self, obj):
        return mark_safe(obj.profiles)

    set_profiles.short_description = '简介'
    list_display = ('id', 'name', 'address', 'set_profiles', 'is_Delete')
    search_fields = ('name',)


admin.site.register(Press, PressAdmin)


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'profiles')
    filter_horizontal = ('book',)
    # raw_id_fields = ("book",)


admin.site.register(Author, AuthorAdmin)


class FamilyAdmin(admin.ModelAdmin):
    search_fields = ('book__name', 'name')
    list_display = ('id', 'name', 'book')
    raw_id_fields = ("book",)


admin.site.register(Family, FamilyAdmin)


class SubsectionAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        lasttime = obj.updateDay
        booklasttime = obj.book.lastUpdated
        if not change or not booklasttime:
            obj.book.lastUpdated = lasttime
            obj.book.save()
        elif booklasttime:
            if booklasttime < lasttime:
                obj.book.lastUpdated = lasttime
                obj.book.save()
        obj.save()
        # Usercollection
        # user = User.userManager.filter(username=username).first()
        collections = Usercollection.UserCollectionManager.filter(
            book=obj.book).all()
        for tmp in collections:
            print(tmp.user.username)
            # Usermessage updateDay
            message = "你的收藏 "+str(obj.book)+"更新了"
            usermessage = Usermessage(
                fromuser=tmp.user, touser=tmp.user, message=message, messagetime=obj.updateDay)
            usermessage.save()

    def get_image(self, obj):
        strtmp = "<img src='{url}' alt='图像' width=50>".format(
            url=obj.image.url)
        return mark_safe(strtmp)

    get_image.short_description = '图片'
    search_fields = ('book__name', 'name')
    list_display = (
        'id', 'book', 'bookNumber', 'name', 'updateDay',
        'get_image', 'physicalFileAddress', 'is_Delete')
    raw_id_fields = ('book',)


admin.site.register(Subsection, SubsectionAdmin)


class BookRankingAdmin(admin.ModelAdmin):
    def calc_average_value(self, obj):
        if not obj.scoreNumber:
            return '暂无评分'
        else:
            return Decimal(obj.scoreValue / obj.scoreNumber).quantize(Decimal('0.0'))

    calc_average_value.short_description = '评分'
    list_display = (
        'id', 'book', 'popularity', 'scoreValue',
        'scoreNumber', 'calc_average_value', 'collection')
    raw_id_fields = ('book',)


admin.site.register(BookRanking, BookRankingAdmin)


class ThisLightNovelIsTerrificAdmin(admin.ModelAdmin):
    list_display = ('id', 'years', 'ranking', 'book')
    search_fields = ('book__name',)
    list_filter = ('years',)
    ordering = ('-years', 'ranking')
    # 将添加元素时外键位变成文本框加选择，而不是以前下拉框
    raw_id_fields = ('book',)


admin.site.register(ThisLightNovelIsTerrific, ThisLightNovelIsTerrificAdmin)
