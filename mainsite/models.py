from django.db import models
from ckeditor.fields import RichTextField
import os
import ReadBooks.settings


class PressManager(models.Manager):
    def get_queryset(self):
        return super(PressManager, self).get_queryset().filter(is_Delete=False)


class Press(models.Model):
    """出版社"""
    # id
    id = models.AutoField(primary_key=True)
    # 名称
    name = models.CharField(max_length=40, null=True,
                            blank=True, unique=True, verbose_name='名称')
    # 地址
    address = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='地址')
    # 简介
    profiles = RichTextField(null=True, blank=True, verbose_name='简介')
    # 逻辑删除
    is_Delete = models.BooleanField(default=False, verbose_name='是否删除')
    # 管理器
    object = models.Manager()
    userManager = PressManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Press'
        verbose_name = '出版社'
        verbose_name_plural = '出版社'


class Family(models.Model):
    """书籍类别"""
    family_choices = (
        ('01', '热血'),
        ('02', '奇幻'),
        ('03', '冒险'),
        ('04', '战斗'),
        ('05', '穿越'),
        ('06', '日常'),
        ('07', '科幻'),
        ('08', '治愈'),
        ('09', '校园'),
        ('10', '恋爱'),
        ('11', '后宫'),
        ('12', '猎奇'),
        ('13', '魔法'),
        ('14', '历史'),
        ('15', '致郁'),
        ('16', '推理'),
        ('17', '智斗'),
        ('18', '装逼'),
        ('19', '职场'),
        ('20', '搞笑'),
    )
    name = models.CharField(
        max_length=4, choices=family_choices, verbose_name='类别')
    book = models.ForeignKey(
        'Book', on_delete=models.CASCADE, verbose_name='书名')
    object = models.Manager()
    userManager = models.Manager()

    def __str__(self):
        return "{name}+{book}".format(name=self.name, book=self.book.name)

    class Meta:
        db_table = 'Family'
        verbose_name = '书籍类别'
        verbose_name_plural = '书籍类别'


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='名字')
    book = models.ManyToManyField('Book', blank=True, verbose_name='书名')
    profiles = RichTextField(null=True, blank=True, verbose_name='简介')
    object = models.Manager()
    userManager = models.Manager()

    def __str__(self):
        return '{name}'.format(name=self.name)

    class Meta:
        db_table = 'Author'
        verbose_name = '作者'
        verbose_name_plural = '作者'


def get_from_book_save_image_path(instance, filename):
    url_path = 'book/%s/images' % instance.name
    loadpath = os.path.join(ReadBooks.settings.MEDIA_ROOT, url_path)
    if not os.path.exists(loadpath):
        os.makedirs(loadpath)
    return url_path + '/%s' % filename


class BookManager(models.Manager):
    def get_queryset(self):
        return super(BookManager, self).get_queryset().filter(is_Delete=False)


class Book(models.Model):
    """书籍"""
    # id
    id = models.AutoField(primary_key=True)
    # 名称
    name = models.CharField(max_length=100, unique=True, verbose_name='名称')
    # 状态
    classify_choices = (
        ('0', '已完结'),
        ('1', '连载中'),
        ('2', '停更'),
        ('3', '未知'),
    )
    state = models.CharField(
        max_length=1, choices=classify_choices, default='3', verbose_name='状态')
    # 图片
    image = models.ImageField(
        upload_to=get_from_book_save_image_path, default='book/defaultpicture.png')
    # 简介
    profiles = RichTextField(verbose_name='简介')
    # 出版日
    publicatioDay = models.DateField(verbose_name='出版日')
    # 最近更新日
    lastUpdated = models.DateTimeField(
        null=True, blank=True, verbose_name='最后更新日')
    # 类别
    # 在Family表中
    # 出版社
    publishers = models.ForeignKey(
        'Press', on_delete=models.DO_NOTHING, verbose_name='出版社')
    # 逻辑删除
    is_Delete = models.BooleanField(default=False, verbose_name='是否删除')
    # 管理器
    object = models.Manager()
    userManager = BookManager()

    def __str__(self):
        return '{name}+{publish}'.format(name=self.name, publish=self.publishers.name)

    class Meta:
        db_table = 'Book'
        verbose_name = '书籍'
        verbose_name_plural = '书籍'


def get_from_subsection_save_image_path(instance, filename):
    url_path = 'book/%s/images' % instance.book.name
    loadpath = os.path.join(ReadBooks.settings.MEDIA_ROOT, url_path)
    if not os.path.exists(loadpath):
        os.makedirs(loadpath)
    return url_path + '/%s' % filename


def get_from_subsection_save_address_path(instance, filename):
    url_path = 'book/%s/text/%s+%s' % (instance.book.name,
                                       instance.bookNumber, instance.name)
    # print(ReadBooks.settings.MEDIA_ROOT)
    loadpath = os.path.join(ReadBooks.settings.MEDIA_ROOT, url_path)
    if not os.path.exists(loadpath):
        os.makedirs(loadpath)
        # print('*/-' * 20)
    return url_path + '/%s' % filename


class SubsectionManager(models.Manager):
    def get_queryset(self):
        return super(SubsectionManager, self).get_queryset().filter(is_Delete=False)


class Subsection(models.Model):
    """分卷"""
    # id
    id = models.AutoField(primary_key=True)
    # 所属书
    book = models.ForeignKey(
        'Book', on_delete=models.CASCADE, verbose_name='所属书名')
    # 卷号
    bookNumber = models.PositiveSmallIntegerField(verbose_name='卷号')
    # 名称
    name = models.CharField(max_length=100, verbose_name='名称')
    # 更新日
    updateDay = models.DateTimeField(verbose_name='更新日期')
    # 图片
    image = models.ImageField(upload_to=get_from_subsection_save_image_path, default='book/defaultpicture.png',
                              verbose_name='图片')
    # 简介
    profiles = RichTextField(verbose_name='简介')
    # 价格
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.0, verbose_name='价格')
    # 优惠
    discount = models.DecimalField(
        max_digits=4, decimal_places=2, default=10.0, verbose_name='优惠')
    # 物理文件地址
    physicalFileAddress = models.FileField(
        upload_to=get_from_subsection_save_address_path, verbose_name='物理地址')
    # 逻辑删除
    is_Delete = models.BooleanField(default=False, verbose_name='是否删除')
    # 管理器
    object = models.Manager()
    userManager = SubsectionManager()

    def __str__(self):
        return '{0}*-*{1}-*-{2}'.format(self.book.name, self.bookNumber, self.name)

    class Meta:
        db_table = 'Subsection'
        verbose_name = '分卷'
        verbose_name_plural = '分卷'


# class Discount(models.Model):
#     """折扣"""
#     # id
#     id = models.AutoField(primary_key=True)
#     # 名称
#     name = models.CharField(max_length=30)
#     # 折扣类型
#     discount_choices = (
#         ('1', "满减"),
#         ('2', "满折"),
#         ('3', "自定义函数"),
#     )
#     discountType = models.CharField(max_length=2)
#     # 算法
#     # 起始日期
#     # 截止日期
#     # 介绍
#     # 数量
class BookRankingManager(models.Manager):
    def get_queryset(self):
        return super(BookRankingManager, self).get_queryset().filter(book__is_Delete=False)

    def createranking(self, book):
        m_book = BookRanking()
        m_book.book = book
        m_book.save()

    def clearRanking(self, rank):
        rank.popularity = 0
        rank.scoreValue = 0
        rank.scoreNumber = 0
        rank.collection = 0
        rank.viewingnumber = 0
        rank.likenumber = 0
        rank.coinnumber = 0
        rank.save()


class BookRanking(models.Model):
    """book排行信息"""
    # 主键
    id = models.AutoField(primary_key=True)
    # 图书id
    book = models.OneToOneField('Book', models.CASCADE, verbose_name='书名')

    popularity = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name='人气')
    scoreValue = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name='评分值')
    scoreNumber = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name='评分数')
    collection = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name='收藏')
    viewingnumber = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name='观看数')
    likenumber = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name='点赞数')
    coinnumber = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name='投币数')

    object = models.Manager()
    userManager = BookRankingManager()

    class Meta:
        db_table = 'BookRanking'
        verbose_name = '图书排行'
        verbose_name_plural = '图书排行'


class ThisLightNovelIsTerrific(models.Model):
    """这本轻小说真厉害"""
    id = models.AutoField(primary_key=True)
    year_choices = (
        ('1', '2005'),
        ('2', '2006'),
        ('3', '2007'),
        ('4', '2008'),
        ('5', '2009'),
        ('6', '2010'),
        ('7', '2011'),
        ('8', '2012'),
        ('9', '2013'),
        ('10', '2014'),
        ('11', '2015'),
        ('12', '2016'),
        ('13', '2017'),
        ('14', '2018'),
        ('15', '2019'),
        ('16', '2020'),
    )
    years = models.CharField(
        max_length=3, choices=year_choices, verbose_name='年份')
    ranking = models.PositiveSmallIntegerField(verbose_name='排名')
    book = models.ForeignKey(
        'Book', on_delete=models.DO_NOTHING, verbose_name='书名')
    object = models.Manager()
    userManager = models.Manager()

    class Meta:
        db_table = 'LightNovelRanking'
        verbose_name = '这本轻小说真厉害'
        verbose_name_plural = '这本轻小说真厉害'
