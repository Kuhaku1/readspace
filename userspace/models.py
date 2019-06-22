from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
import datetime
from mainsite.models import Book
from mainsite.models import Subsection


class UserManager(models.Manager):
    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(is_Delete=False)

    def create_user(self, username, password, name):
        user = User()
        user.username = username
        user.password = password
        user.name = name
        user.save()

        userbalance = Userbalance()
        userbalance.user = user
        userbalance.save()

        usergrade = Usergrade()
        usergrade.user = user
        usergrade.save()


class User(models.Model):
    """用户"""
    # id
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=30, verbose_name='密码')
    name = models.CharField(max_length=30, verbose_name='姓名')

    address = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='地址')
    # 联系方式
    contact = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='手机号')
    # 邮箱
    mailbox = models.CharField(
        max_length=30, null=True, blank=True, verbose_name='邮箱')
    # 签名 （介绍）
    profiles = RichTextField(verbose_name='签名', null=True, blank=True,)

    # 逻辑删除
    is_Delete = models.BooleanField(default=False, verbose_name='是否删除')
    # 管理器

    object = models.Manager()

    userManager = UserManager()

    def __str__(self):
        return '{0}*-*{1}-*-{2}'.format(self.username, self.name, self.is_Delete)

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'


def settime_asvip():
    return datetime.datetime.strptime('1-1-1970 8:0:0', '%m-%d-%Y %H:%M:%S')


class Userbalance(models.Model):
    """用户余额"""
    # id
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, verbose_name='用户')
    # 余额
    money = models.PositiveIntegerField(default=0, verbose_name='余额')
    # 硬币
    coin = models.PositiveIntegerField(default=0, verbose_name='硬币')

    is_vip = models.BooleanField(default=False, verbose_name='是否是vip')
    expirationdate = models.DateTimeField(
        default=settime_asvip, verbose_name='vip过期时间')

    object = models.Manager()

    def __str__(self):
        return '{0}*-*{1}-*-{2}'.format(self.user.username, self.money, self.coin)

    class Meta:
        db_table = 'userbalance'
        verbose_name = '用户余额'
        verbose_name_plural = '用户余额'


class Usergrade(models.Model):
    """用户等级"""
    # id
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, verbose_name='用户')
    # 等级
    grade = models.PositiveIntegerField(default=0, verbose_name='等级')
    # 阅读时间
    readtime = models.PositiveIntegerField(default=0, verbose_name='阅读时间')
    # 经验值
    experience = models.PositiveIntegerField(default=0, verbose_name='经验值')

    object = models.Manager()

    def __str__(self):
        return '{0}*-*{1}-*-{2}'.format(self.user.username, self.grade, self.readtime)

    class Meta:
        db_table = 'usergrade'
        verbose_name = '用户等级'
        verbose_name_plural = '用户等级'


class Userhistroy(models.Model):
    """用户历史"""
    # id
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, verbose_name='用户')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name='图书')
    subsection = models.ForeignKey(
        Subsection, on_delete=models.CASCADE, verbose_name='分卷')

    lastUpdated = models.DateTimeField(
        null=True, blank=True, verbose_name='状态更新时间')

    object = models.Manager()

    def __str__(self):
        return '{0}*-*{1}-*-{2}'.format(self.user.username, self.book.name, self.subsection.bookNumber)

    class Meta:
        db_table = 'userhistroy'
        verbose_name = '用户历史'
        verbose_name_plural = '用户历史'


class CollectionManager(models.Manager):
    def get_queryset(self):
        return super(CollectionManager, self).get_queryset().filter(event="coll")


class CoinManager(models.Manager):
    def get_queryset(self):
        return super(CoinManager, self).get_queryset().filter(event="coin")


class LikesManager(models.Manager):
    def get_queryset(self):
        return super(LikesManager, self).get_queryset().filter(event="like")


class Usercollection(models.Model):
    """用户收藏"""
    # id
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, verbose_name='用户')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name='图书')
    collectiontime = models.DateTimeField(
        null=True, blank=True, verbose_name='收藏时间')

    collection = "coll"
    likes = "like"
    coin = "coin"
    event_choices = (
        (collection, "收藏"),
        (likes, "点赞"),
        (coin, "投币"),
    )
    event = models.CharField(
        max_length=5, choices=event_choices, verbose_name='事件', default=collection)
    object = models.Manager()
    UserCollectionManager = CollectionManager()
    UserLikesManager = LikesManager()
    UserCoinManager = CoinManager()

    def __str__(self):
        return '{0}*-*{1}-*-{2}'.format(self.user.username, self.book.name, self.collectiontime)

    class Meta:
        db_table = 'usercollection'
        verbose_name = '用户收藏'
        verbose_name_plural = '用户收藏'


class UsermessageManager(models.Manager):
    def get_queryset(self):
        return super(UsermessageManager, self).get_queryset().filter(is_Delete=False)


class Usermessage(models.Model):
    """用户消息"""
    # id
    id = models.AutoField(primary_key=True)
    fromuser = models.ForeignKey(
        User, related_name="from_message", on_delete=models.CASCADE, verbose_name='消息发送者')

    touser = models.ForeignKey(
        User, related_name="to_message", on_delete=models.CASCADE, verbose_name='消息接受者')

    message = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='消息内容')

    messagetime = models.DateTimeField(
        null=True, blank=True, verbose_name='创建时间')
    is_Delete = models.BooleanField(default=False, verbose_name='是否删除')
    is_views = models.BooleanField(default=False, verbose_name='是否查看')

    object = models.Manager()
    userManager = UsermessageManager()

    def __str__(self):
        return '{0}*-*{1}-*-{2}'.format(self.fromuser.username, self.touser.username,
                                        self.message, self.messagetime)

    class Meta:
        db_table = 'usermessage'
        verbose_name = '用户消息'
        verbose_name_plural = '用户消息'


class Userreadtime(models.Model):
    """用户每月的阅读时间统计"""
    # id
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='用户')
    sumtime = models.IntegerField(verbose_name='本月的阅读时间')
    lasttime = models.IntegerField(verbose_name='状态最后更新时间戳')

    object = models.Manager()

    def __str__(self):
        return '{0}*-*{1}'.format(self.user.username, self.sumtime)

    class Meta:
        db_table = 'userreadtime'
        verbose_name = '用户每月的阅读时间统计'
        verbose_name_plural = '用户每月的阅读时间统计'


class UsercommentManager(models.Manager):
    def get_queryset(self):
        return super(UsercommentManager, self).get_queryset().filter(is_Delete=False)


class Usercomment(models.Model):
    """用户评论"""
    # id
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='评论者')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name='评论的书')
    comment = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='评论内容')

    commenttime = models.DateTimeField(
        null=True, blank=True, verbose_name='创建时间')
    is_Delete = models.BooleanField(default=False, verbose_name='是否删除')

    object = models.Manager()
    userManager = UsercommentManager()

    def __str__(self):
        return '{0}*-*{1}-*-{2}'.format(self.user.username, self.comment, self.commenttime)

    class Meta:
        db_table = 'usercomment'
        verbose_name = '用户评论'
        verbose_name_plural = '用户评论'
