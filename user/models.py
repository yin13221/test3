from django.db import models


# Create your models here.
class User(models.Model):
    tel = models.CharField(unique=True, max_length=11, verbose_name="手机号")
    password = models.CharField(max_length=32, verbose_name="密码")
    status = models.IntegerField(blank=True, null=True, verbose_name="状态")
    reg_time = models.DateTimeField(blank=True, null=True, verbose_name="注册时间")
    alipay_user_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="支付宝的用户ID")
    qq_user_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="QQ的用户ID")
    wx_user_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="微信的用户ID")

    class Meta:
        managed = False
        db_table = 't_user'


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name="角色名")
    users = models.ManyToManyField(to=User, db_table="t_role_user", blank=True, null=True, related_name="roles")

    class Meta:
        db_table = "t_role"


class UserInfo(models.Model):
    email = models.CharField(max_length=50, verbose_name="邮箱")
    birth = models.DateField(blank=True, null=True, verbose_name="出生日期")
    nickname = models.CharField(max_length=100, blank=True, null=True, verbose_name="昵称")
    realname = models.CharField(max_length=100, blank=True, null=True, verbose_name="真实姓名")
    sex = models.CharField(max_length=1, blank=True, null=True, verbose_name="性别")
    photo = models.BinaryField(blank=True, null=True, verbose_name="头像")
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='info', blank=True)

    class Meta:
        managed = False
        db_table = 't_user_info'


class UserScore(models.Model):
    score = models.IntegerField(blank=True, null=True, verbose_name="分数")
    remark = models.CharField(max_length=100, blank=True, null=True, verbose_name="积分来源")
    create_time = models.DateTimeField(blank=True, null=True, verbose_name="创建时间")
    user = models.OneToOneField(to=User, blank=True, null=True, on_delete=models.CASCADE, related_name="score")

    class Meta:
        managed = False
        db_table = 't_user_score'


class UserFriend(models.Model):
    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.CASCADE, related_name="users")
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user_friend'


class Logger(models.Model):
    realname = models.CharField(max_length=100, blank=True, null=True)
    func_name = models.CharField(max_length=200, blank=True, null=True)
    func_param = models.CharField(max_length=200, blank=True, null=True)
    request_url = models.CharField(max_length=100, blank=True, null=True)
    exception_code = models.CharField(max_length=20, blank=True, null=True)
    exception_msg = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 't_logger'
