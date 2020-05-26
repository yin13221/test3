# Generated by Django 3.0 on 2019-12-31 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel', models.CharField(max_length=11, unique=True, verbose_name='手机号')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('status', models.IntegerField(blank=True, null=True, verbose_name='状态')),
                ('reg_time', models.DateTimeField(blank=True, null=True, verbose_name='注册时间')),
                ('alipay_user_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='支付宝的用户ID')),
                ('qq_user_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='QQ的用户ID')),
                ('wx_user_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='微信的用户ID')),
            ],
            options={
                'db_table': 't_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserFriend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 't_user_friend',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50, verbose_name='邮箱')),
                ('birth', models.DateField(blank=True, null=True, verbose_name='出生日期')),
                ('nickname', models.CharField(blank=True, max_length=100, null=True, verbose_name='昵称')),
                ('realname', models.CharField(blank=True, max_length=100, null=True, verbose_name='真实姓名')),
                ('sex', models.CharField(blank=True, max_length=1, null=True, verbose_name='性别')),
                ('photo', models.BinaryField(blank=True, null=True, verbose_name='头像')),
            ],
            options={
                'db_table': 't_user_info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(blank=True, null=True, verbose_name='分数')),
                ('remark', models.CharField(blank=True, max_length=100, null=True, verbose_name='积分来源')),
                ('create_time', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
            ],
            options={
                'db_table': 't_user_score',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='角色名')),
                ('users', models.ManyToManyField(blank=True, db_table='t_role_user', null=True, related_name='roles', to='user.User')),
            ],
            options={
                'db_table': 't_role',
            },
        ),
    ]