# Generated by Django 2.1.7 on 2019-05-17 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userspace', '0005_auto_20190503_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercollection',
            name='event',
            field=models.CharField(choices=[('coll', '收藏'), ('like', '点赞'), ('coin', '投币')], default='coll', max_length=5, verbose_name='事件'),
        ),
    ]
