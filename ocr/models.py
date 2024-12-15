from django.db import models
from django.utils import timezone

class OCRUser(models.Model):
    username = models.CharField(max_length=150, unique=True)  # 用户名，唯一
    password = models.CharField(max_length=128)  # 密码字段


class OCRImage(models.Model):
    image = models.ImageField(upload_to='images/', default='test.png')  # 使用 ImageField 存储图片路径
    owner = models.ForeignKey('OCRUser', on_delete=models.CASCADE)  # 外键关联到 User 表
    recognition_result = models.TextField(blank=True, null=True)  # 存储识别结果，可以为空
    recognition_time = models.DateTimeField(default=timezone.now)  # 存储识别时间，默认为当前时间

    def __str__(self):
        return f"{self.owner.username}'s image"
