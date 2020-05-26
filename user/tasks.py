from py1909_lovedown import celery_app
from datetime import datetime

from django.core.mail import EmailMessage


@celery_app.task
def celery_async_send_mail(password, nickname, email):
    time = datetime.now()
    time = time.strftime("Y-m-d %H:%M:%S")

    body = f"""
                <p>尊敬的{nickname},您于{time}在本网站进行密码的找回，您的新密码是<span style="color:red;">{password}</span></p>
                <p>如果不是您本人操作，请尽快到网站中，修改您的密码，以保证您的账户安全</p>
            """

    message = EmailMessage(subject='爱下载-找回密码', body=body, to=[email])
    message.content_subtype = 'html'
    message.send()
