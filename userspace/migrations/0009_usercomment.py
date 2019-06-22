# Generated by Django 2.1.7 on 2019-06-09 02:29

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0002_auto_20190530_1730'),
        ('userspace', '0008_userreadtime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usercomment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(blank=True, max_length=100, null=True, verbose_name='评论内容')),
                ('commenttime', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('is_Delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.Book', verbose_name='评论的书')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userspace.User', verbose_name='评论者')),
            ],
            options={
                'verbose_name': '用户评论',
                'verbose_name_plural': '用户评论',
                'db_table': 'usercomment',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]