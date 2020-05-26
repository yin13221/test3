"""py1909_lovedown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^$', view.index, name="index"),
    path('register', view.register, name='register'),
    path('next/<int:user_id>', view.next, name='next'),
    path('check/<tel>', view.check_tel, name='check_tel'),
    path('point', view.point, name='point'),
    path('login', view.login, name='login'),
    path('logout', view.logout, name='logout'),
    path('photo', view.photo, name='photo'),
    path('mine', view.mine, name='mine'),
    path('change_pwd', view.change_pwd, name='change_pwd'),
    url('^user/', include('user.urls')),
    url('^res/', include('resource.urls')),
    url('^third/', include('third.urls')),
    url('^bbs/', include('bbs.urls')),
    path('findpass', view.findpass, name='findpass'),
    path('shoucang', view.shoucang, name='shoucang')
]
