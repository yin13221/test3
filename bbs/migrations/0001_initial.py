# Generated by Django 3.0 on 2019-12-30 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bbs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bbs_type', models.CharField(max_length=100, verbose_name='帖子类型')),
                ('subject', models.CharField(max_length=200, verbose_name='帖子标题')),
                ('content', models.TextField(verbose_name='帖子正文内容')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('user_id', models.IntegerField(verbose_name='发帖子')),
                ('top', models.CharField(choices=[('1', '是'), ('0', '否')], max_length=20, verbose_name='是否置顶')),
            ],
            options={
                'db_table': 't_bbs',
            },
        ),
    ]
