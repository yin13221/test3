import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'py1909_lovedown.settings')

app = Celery("py1909_lovedown", broker="redis://127.0.0.1:6379/6", backend="redis://127.0.0.1:6379/7")

# 让 celery 自动发现任务,会找 INSTALLED_APPS 应用下的 tasks.py 文件
app.autodiscover_tasks()

