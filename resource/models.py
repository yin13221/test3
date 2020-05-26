from django.db import models
from user.models import User


# Create your models here.
class Resource(models.Model):
    res_name = models.CharField(max_length=100, blank=True, null=True)
    __resource_type = (
        ("文本文件", "文本文件"),
        ("电子文件", "电子文件"),
        ("压缩文件", "压缩文件"),
    )
    res_type = models.CharField(max_length=30, choices=__resource_type, blank=True, null=True, verbose_name="资源类型")
    keyword = models.CharField(max_length=50, blank=True, null=True, verbose_name="关键字")
    score = models.IntegerField(blank=True, null=True, verbose_name="资源积分")
    res_desc = models.TextField(blank=True, null=True, verbose_name="资源描述")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='resources', blank=True, null=True)
    ext = models.CharField(max_length=20, blank=True, null=True, verbose_name="资源后缀")
    upload_time = models.DateTimeField(blank=True, null=True, verbose_name="上传时间", auto_now=True)
    size = models.IntegerField(blank=True, null=True, verbose_name="资源大小")
    res_address = models.FileField(upload_to='media/resource', max_length=200, blank=True, null=True,
                                   verbose_name="资源路径")
    content_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="资源类型")

    class Meta:
        managed = False
        db_table = 't_resource'


class ResourceDownload(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="downloads", blank=True, null=True,
                             verbose_name="下载资源的用户ID")
    res = models.ForeignKey(to=Resource, on_delete=models.CASCADE, related_name="downloads", blank=True, null=True,
                            verbose_name="资源ID")
    download_time = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="下载时间")

    class Meta:
        managed = False
        db_table = 't_resource_download'


class ResourceComment(models.Model):
    star = models.IntegerField(blank=True, null=True, verbose_name="星级")
    content = models.TextField(blank=True, null=True, verbose_name="评论内容")
    comment_time = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="评论时间")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments", blank=True, null=True,
                             verbose_name="评论的用户ID")
    res = models.ForeignKey(to=Resource, on_delete=models.CASCADE, related_name="comments", blank=True, null=True,
                            verbose_name="资源ID")

    class Meta:
        managed = False
        db_table = 't_resource_comment'


class ResourceCollect(models.Model):
    res = models.ForeignKey(to=Resource, on_delete=models.CASCADE, related_name="collect", blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="collect", blank=True, null=True)
    collect_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_resource_collect'
