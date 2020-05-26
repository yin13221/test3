from django.core.paginator import Paginator
from django.shortcuts import render
from bbs.models import Bbs
from django.http import JsonResponse
from py1909_lovedown.decorators import auth_session
from py1909_lovedown import db
from user.models import User
from django.forms import model_to_dict
from .froms import BbsFrom


def index(request):
    queryset = Bbs.objects.all().order_by("-top", "-create_time")
    paginator = Paginator(queryset, 10)
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)
    return render(request, "bbs.html", {"data": page})


@auth_session
def tz(request):
    # param = request.POST.dict()
    # user_id = db.get_current_user_id(request)
    # user = User.objects.get(pk=user_id)
    # param.setdefault("user", user)
    # bbs = Bbs.objects.create(**param)
    # nickname = bbs.user.info.nickname
    # create_time = bbs.create_time
    # bbs = model_to_dict(bbs)
    # bbs["nickname"] = nickname
    # bbs["create_time"] = create_time
    # return JsonResponse(bbs)
    form = BbsFrom(request.POST)
    if form.is_valid():
        user_id = db.get_current_user_id(request)
        user = User.objects.get(pk=user_id)
        bbs = form.instance
        bbs.user = user
        bbs.save()

        nickname = bbs.user.info.nickname
        create_time = bbs.create_time
        bbs = model_to_dict(bbs)
        bbs["nickname"] = nickname
        bbs["create_time"] = create_time
        return JsonResponse(bbs)
    errors = form.errors
    return JsonResponse(errors)
