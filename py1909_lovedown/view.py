from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.utils.http import urlquote
from django.core.paginator import Paginator

from . import db
from .decorators import score_setting, auth_session
from user import tasks
from user.forms import UserModelForm
from hashlib import md5
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django_redis import get_redis_connection
from django.core.cache import cache

redis = get_redis_connection()

# redis.set("a", 3)


def index(request):
    try:
        # 获取用户是否登录的信息
        msg = request.session.pop("msg")
    except:
        msg = None
    sql = """
            select t.id, t.res_name, 
                t.score, t.upload_time,  t.ext ,
                f.nickname from t_resource t left join t_user_info f
                on t.user_id = f.user_id order by t.upload_time desc
    """

    data = db.query_list(sql)
    paginator = Paginator(data, 10)
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)

    return render(request, "index.html", {"msg": msg, "data": page})


@auth_session
def point(request):
    user_id = db.get_current_user_id(request)
    sql = "select * from t_user_score where user_id = %s"
    scores = db.query_list(sql, args=(user_id,))
    sql = "select sum(score) sum from t_user_score where user_id = %s"
    score_sum = db.query_one(sql, args=(user_id,))
    return render(request, 'point.html', {"scores": scores, "score_sum": score_sum})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    # param = request.POST.dict()
    # # 2、处理业务逻辑
    # ## 2.1 根据手机号，查询该手机号是否已经被注册
    # sql = "select * from t_user where tel = %s"
    # user = db.query_one(sql, args=(param.get("tel"),))
    # # 如果  user 为None , 代表可以注册
    # if user is not None:
    #     param["msg"] = "手机号已被注册"
    #     return render(request, "register.html", param)
    # # 进行注册
    # sql = "insert into t_user(tel, password, status, reg_time) values(%(tel)s, md5(%(password)s), 1, now())"
    # pk = db.update(sql, args=param)
    # # 获取 第三方登录的 type 和 ID
    # types = param.get("type")
    # third_user_id = param.get("third_user_id")
    #
    # if types and third_user_id:
    #     # 更新字段
    #     column = "alipay_user_id" if types == "1" else "qq_user_id" if types == "2" else "wx_user_id"
    #     sql = f"update t_user set {column} = %s where id = %s"
    #     db.update(sql, args=(third_user_id, pk))
    #
    # # 页面进行跳转，进行下一步操作
    # return render(request, "next.html", {"user_id": pk})

    form = UserModelForm(request.POST)
    # 对页面参数进行校验
    if form.is_valid():

        user = form.instance
        # 获取页面的密码
        password = user.password
        # 对密码进行MD5加密
        password = md5(password.encode()).hexdigest()
        user.password = password
        # 将数据保存到表中
        form.save()
        # 获取模型对象的主键
        pk = user.pk

        param = request.POST.dict()
        # 获取 第三方登录的 type 和 ID
        type = param.get("type")
        third_user_id = param.get("third_user_id")

        if type and third_user_id:
            # 更新字段
            column = "alipay_user_id" if type == "1" else "qq_user_id" if type == "2" else "wx_user_id"
            sql = f"update t_user set {column} = %s where id = %s"
            db.update(sql, args=(third_user_id, pk))

        # 页面进行跳转，进行下一步操作
        return render(request, "next.html", {"user_id": pk})

    else:
        pass


@score_setting(action="用户注册")
def next(request, user_id):
    if request.method == "GET":
        return render(request, 'next.html')

    photo = request.FILES.get("photo")
    _photo = photo.read()
    param = request.POST.dict()
    param.setdefault("photo", _photo)
    param.setdefault("user_id", user_id)

    sql = "insert into t_user_info(email,birth,nickname,realname,sex,photo,user_id) values (%(email)s,%(birth)s,%(nickname)s,%(realname)s,%(sex)s,%(photo)s,%(user_id)s)"
    db.update(sql, args=param)

    sql = "update t_user set status=2 where id = %s"
    db.update(sql, args=(user_id,))
    return render(request, "success.html", {"userID": user_id, "nickname": param.get("nickname")})


def check_tel(request, tel):
    sql = "select * from t_user where tel=%s"
    user = db.query_one(sql, args=(tel,))
    if user is None:
        return JsonResponse({"status": True, "msg": ""})
    return JsonResponse({"status": False, "msg": "手机号已被注册"})


# @csrf_exempt
def login(request):
    param = request.POST.dict()
    sql = 'select * from t_user where tel = %(tel)s and password = md5(%(password)s)'
    user = db.query_one(sql, args=param)

    if user is None:
        return render(request, "index.html", {"msg": "账户或密码错误", "tel": param.get("tel")})
    if user.get("status") == 1:
        return render(request, "next.html", {"user_id": user.get("id")})
    if user.get("status") == 3:
        return render(request, "index.html", {"msg": "您的账号已被冻结，请联系管理员", "tel": param.get("tel")})

    # user.pop("reg_time")
    request.session["LOGIN_LOCAL_FLAG"] = user

    # 获取 要跳转的页面
    url = request.POST.get("url")

    if not url:
        # 5. 登录成功
        return redirect(to=reverse("index"))

    return redirect(to=url)


def logout(request):
    request.session.clear_expired()
    request.session.flush()
    return redirect(to='/')


def findpass(request):
    if request.method == "GET":
        return render(request, "findpass.html")

    type = request.POST.get("type")
    tel = request.POST.get("tel")
    certificate = request.POST.get("certificate")

    if type == "email":
        email = certificate
        sql = "select t.*,f.email,f.nickname from t_user t left join t_user_info f on t.id = f.user_id where t.tel = %s"
        user = db.query_one(sql, args=(tel,))
        if user is None:
            return JsonResponse({"msg": "账号不存在"})
        if email != user.get("email"):
            return JsonResponse({"msg": "邮箱必须是注册的时候绑定的邮箱"})

        import string, random
        string_random = string.ascii_letters + string.digits
        password = random.choices(string_random, k=6)
        password = ''.join(password)

        tasks.celery_async_send_mail.delay(password, user.get("nickname"), email)

        sql = 'update t_user set password = md5(%s) where tel = %s'
        db.update(sql, args=(password, tel))

        # request.session["msg"] = "邮件已发送，请用新密码登录"
        return JsonResponse({"msg": "邮件已发送，请用新密码登录"})


@auth_session
def photo(request):
    userID = db.get_current_user_id(request)
    sql = 'select photo from t_user_info where user_id = %s'
    user = db.query_one(sql, args=(userID,))
    photo = user.get("photo")
    response = HttpResponse(photo, content_type='image/png')
    filename = "小可爱.png"
    filename = urlquote(filename)
    response["Content-Disposition"] = "inline;filename=" + filename
    return response


@auth_session
def mine(request):
    userID = db.get_current_user_id(request)
    sql = 'select * from t_user_info where user_id = %s'
    user = db.query_one(sql, args=(userID,))
    sql = 'select score from t_user_score where user_id=%s'
    score = db.query_list(sql, args=(userID,))
    s = 0
    for i in range(len(score)):
        s += score[i]['score']
    user.setdefault("score", s)

    return render(request, 'mine.html', user)


def change_pwd(request):
    return render(request, 'change_pwd.html')


def shoucang(request):
    sql = """
                select t.id, t.res_name, 
                    t.score, t.upload_time,  t.ext ,
                    f.nickname from t_resource t left join t_user_info f
                    on t.user_id = f.user_id order by t.upload_time desc
        """

    data = db.query_list(sql)

    paginator = Paginator(data, 10)
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)

    return render(request, "shoucang.html", {"data": page})
