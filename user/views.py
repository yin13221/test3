from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from py1909_lovedown import db


def photo(request, pk):
    sql = "select photo from t_user_info where user_id = %s"

    user = db.query_one(sql, args=(pk,))
    # 获取头像
    photo = user.get("photo")

    return HttpResponse(photo, content_type="image/png")



