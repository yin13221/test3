from alipay.aop.api.domain.AlipayOpenAuthTokenAppModel import AlipayOpenAuthTokenAppModel
from alipay.aop.api.request.AlipayOpenAuthTokenAppRequest import AlipayOpenAuthTokenAppRequest
from alipay.aop.api.response.AlipayOpenAuthTokenAppResponse import AlipayOpenAuthTokenAppResponse
from django.shortcuts import render, redirect
from . import zfb_conf
from django.utils.http import urlquote
from py1909_lovedown import db


# Create your views here.
def zfb(request):
    app_id = zfb_conf.APPID
    login_url = zfb_conf.LOGIN_URL
    redirect_url = urlquote(zfb_conf.REDIRECT_URL)
    return redirect(to=f'{login_url}?app_id={app_id}&redirect_uri={redirect_url}')


def callback(request):
    # 获取支付宝授权码
    app_auth_code = request.GET.get("app_auth_code")
    # 直接获取 客户端对象
    alipay_client = zfb_conf.get_alipay_client()
    # 创建一个接口对应的模型对象，用来接收接口需要的参数
    biz_model = AlipayOpenAuthTokenAppModel()
    biz_model.grant_type = "authorization_code"
    biz_model.code = app_auth_code
    # 创建一个 接口对应的请求对象,
    alipay_request = AlipayOpenAuthTokenAppRequest(biz_model=biz_model)
    # 调用接口
    response_content = alipay_client.execute(alipay_request)
    # 创建一个响应对象，用来处理接口返回的内容
    alipay_response = AlipayOpenAuthTokenAppResponse()
    # 处理结果
    alipay_response.parse_response_content(response_content)
    # 获取 支付宝的用户ID
    if alipay_response.is_success():
        alipay_user_id = alipay_response.user_id
        # 根据支付宝用户ID ，查询该用户是否和本网站的账号进行了绑定
        sql = "select * from t_user where alipay_user_id = %s"
        user = db.query_one(sql, args=(alipay_user_id,))
        if user is None:
            return render(request, 'bind.html', {"alipay_user_id": alipay_user_id})

        if user.get("status") == 1:
            return render(request, "next.html", {"user_id": user.get("id")})
        if user.get("status") == 3:
            return render(request, "index.html", {"msg": "您的账号已被冻结，请联系管理员", "tel": user.get("tel")})

        request.session["LOGIN_LOCAL_FLAG"] = user
        return redirect(to='/')

    request.session["mag"] = "支付宝登陆失败，请重试"
    return redirect(to='/')


def bind(request):
    param = request.POST.dict()

    sql = 'select * from t_user where tel = %(tel)s and password = md5(%(password)s)'
    user = db.query_one(sql, args=param)

    if user is None:
        param.setdefault("msg", "绑定的账号有误")
        return render(request, "bind.html", param)

    sql = "update t_user set "
    if param.get("alipay_user_id"):
        sql += "alipay_user_id = %s where id = %s"
        db.update(sql, args=(param.get("alipay_user_id"), user.get("id")))
    elif param.get("qq_user_id"):
        sql += "qq_user_id = %s where id = %s"
        db.update(sql, args=(param.get("qq_user_id"), user.get("id")))
    else:
        sql += "wx_user_id = %s where id = %s"
        db.update(sql, args=(param.get("wx_user_id"), user.get("id")))

    if user.get("status") == 1:
        return render(request, "next.html", {"user_id": user.get("id")})
    if user.get("status") == 3:
        return render(request, "index.html", {"msg": "您的账号已被冻结，请联系管理员", "tel": user.get("tel")})

    request.session["LOGIN_LOCAL_FLAG"] = user
    return redirect(to='/')


def thrid_register(request):
    # 获取 登录的类型， 1 支付宝， 2 QQ ,3 微信
    param = request.GET.dict()
    # 跳转到注册页面，进行注册
    return render(request, "register.html", param)
