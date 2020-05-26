from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.http import urlquote

from . import db


def score_setting(action):
    def setting_score(func):
        def setting_score_wrapper(request, *args, **kwargs):
            # 调用视图函数
            response = func(request, *args, **kwargs)

            # 从积分配置表中，查询当前动作对应的积分
            sql = "select * from t_score_conf where action = %s"

            conf = db.query_one(sql, args=(action,))

            if conf is None:
                return response
            # 赠送积分
            user_id = kwargs.get("user_id")

            if user_id is not None:
                # 赠送积分
                sql = "insert into t_user_score(score, remark, create_time, user_id) values(%s, %s, now(), %s)"

                db.update(sql, args=(conf.get("score"), action, user_id))

                return response

            # 如果user_id 是 None, 后续学习过 session在处理
            return response

        return setting_score_wrapper

    return setting_score


def auth_session(func):
    def auth_session_wrapper(request, *args, **kwargs):

        # 验证用户是否登录
        if not request.session.has_key("LOGIN_LOCAL_FLAG"):
            request.session["msg"] = "未登录、请登录"
            # 获取 当前动作的来源 地址
            referer = request.headers.get("referer", None)
            if referer is None:
                return redirect(to="/")

            # 判断请求属于同步请求还是异步请求，如果是同步请求，则原逻辑不变，如果异步请求，需要特殊处理
            if "X-Requested-With" in request.headers:
                # 假设 318 是代表 未登录
                return JsonResponse({"url": referer}, status=318)

            return redirect(to="/?url=" + urlquote(referer))

        # 设置存活时间 为 30分钟
        lifetime = settings.SESSION_COOKIE_AGE
        request.session.set_expiry(lifetime)
        request.session.clear_expired()

        # 如果 用户 登录了， 允许 访问 受保护的资源
        return func(request, *args, **kwargs)

    return auth_session_wrapper
