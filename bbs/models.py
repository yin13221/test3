from django.db import models
from user.models import User


class Bbs(models.Model):
    bbs_type = models.CharField(max_length=100, verbose_name="帖子类型")
    subject = models.CharField(max_length=200, verbose_name="帖子标题")
    content = models.TextField(verbose_name="帖子正文内容")
    create_time = models.DateTimeField(auto_now=True)
    # user_id = models.IntegerField(verbose_name="发帖子")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True)
    __top_type = (
        ("1", "是"),
        ("0", "否")
    )
    top = models.CharField(max_length=20, verbose_name="是否置顶", blank=True, null=True, choices=__top_type, default='')

    class Meta:
        db_table = 't_bbs'
        verbose_name = "帖子"
        verbose_name_plural = "帖子"
