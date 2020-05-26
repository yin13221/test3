from uuid import uuid4
from django.shortcuts import render, redirect
from py1909_lovedown import db
from django.http import HttpResponse, JsonResponse
from py1909_lovedown.decorators import auth_session, score_setting
from user.models import User
from resource.forms import ResourceModelForm


@auth_session
def upload(request):
    if request.method == "GET":
        return render(request, 'upload.html')

        # 处理上传逻辑
        # 1、获取页面参数
    # param = request.POST.dict()
    #
    # # 2. 获取上传的资源
    # resource_file = request.FILES.get("res_address")
    #
    # # 通过 UUID生成存储的文件名
    # filename = "media/resource/" + uuid4().hex
    # # 3. 通过 resource_file 的 chunks方法，将上传的文件写入到 磁盘上
    # with open(filename, "wb") as f:
    #     for bytes_file in resource_file.chunks():
    #         f.write(bytes_file)
    #
    # # 4. 将数据写入到数据库中
    # param["res_address"] = filename
    #
    # # 5. 将当前用户ID 绑定到资源中
    # param["user_id"] = db.get_current_user_id(request)
    #
    # # 设置后缀
    # fname = resource_file.name
    # index = fname.rfind(".")
    # ext = fname[index + 1:]
    # param["ext"] = ext
    #
    # param["size"] = resource_file.size
    #
    # param["content_type"] = resource_file.content_type
    #
    # sql = """
    #     insert into t_resource(
    #           res_name, res_type, keyword ,score, res_desc, user_id,
    #           ext, upload_time, size, res_address, content_type
    #         ) values(
    #             %(res_name)s,  %(res_type)s , %(keyword)s, %(score)s,
    #             %(res_desc)s, %(user_id)s, %(ext)s, now(), %(size)s,
    #             %(res_address)s , %(content_type)s
    #         )
    # """
    #
    # # 执行SQL
    # db.update(sql, args=param)
    #
    # return redirect(to="/")

    form = ResourceModelForm(request.POST, files=request.FILES)

    # 对表单进行校验
    form.is_valid()

    # 进行数据的保存， 获取资源模型
    resource = form.instance

    # 获取当前登录的用户ID
    user_id = db.get_current_user_id(request)
    # 获取对应的用户模型
    user = User.objects.get(pk=user_id)

    resource.user = user

    # 获取资源后缀
    resource_file = request.FILES.get("res_address")
    fname = resource_file.name
    index = fname.rfind(".")
    ext = fname[index + 1:]

    resource.ext = ext

    resource.size = resource_file.size

    resource.content_type = resource_file.content_type

    resource.save()

    return redirect(to="/")


def detail(request, pk):
    download_msg = request.session.pop("download_msg", default=None)

    sql = """
        select t.id, t.res_name, t.keyword, t.res_desc ,
            t.score, t.upload_time,  t.ext , t.size , t.user_id ,
            f.nickname , 	
    				(select count(1) from t_resource_download d where d.res_id = t.id) download_num		
    	from t_resource t left join t_user_info f
            on t.user_id = f.user_id 
             where t.id = %s
        """

    resource = db.query_one(sql, args=(pk,))

    # 根据资源ID ,查询该资源的评论
    sql = "select t.*,f.nickname from t_resource_comment t left join t_user_info f on t.user_id = f.user_id where t.res_id = %s"
    comments = db.query_list(sql, args=(pk,))

    # 查询 资源的 星级
    res_star = db.query_proc_one("get_res_star2", args=(pk,))

    star = 0 if res_star is None else res_star.get("v_s")
    # 响应到详情页
    return render(request, "detail.html",
                  {"resource": resource, "LOGIN_LOCAL_FLAG": download_msg, "comments": comments, "star": star})


@auth_session
def download(request, pk):
    sql = "select * from t_resource where id = %s"
    res = db.query_one(sql, args=(pk,))
    user_id = db.get_current_user_id(request)
    if res.get("user_id") != user_id:
        if res.get("score") > 0:
            sql = "select sum(score) sum from t_user_score where user_id = %s"
            user_score = db.query_one(sql, args=(user_id,))
            sum_score = user_score.get("sum")
            if sum_score < res.get("score"):
                request.session.setdefault("download_msg", "您的积分不足")
                return redirect(to="res:detail", **{"pk": pk})

            sql = """
                select count(1) count from t_resource_download where user_id = %s
                    and res_id = %s and download_time >= DATE_SUB(now(),INTERVAL 1 MONTH)
            """
            last_month_down_count = db.query_one(sql, args=(user_id, pk)).get("count")
            if last_month_down_count == 0:
                sql = "insert into t_user_score(score, remark,create_time,user_id) values (%s,%s,now(),%s)"

                db.update(sql, args=(int(res.get("score")) * -1, "资源下载", user_id))
                db.update(sql, args=(int(res.get("score")), "下载资源", res.get("user_id")))
        sql = "insert into t_resource_download(user_id,res_id,download_time) values (%s,%s,now())"
        db.update(sql, args=(user_id, pk))
    resource_path = res.get("res_address")
    with open(resource_path, "rb") as f_r:
        file_bytes = f_r.read()

        response = HttpResponse(file_bytes, content_type=res.get("content_type"))

        filename = f"{res.get('res_name')}.{res.get('ext')}"
        from django.utils.http import urlquote
        filename = urlquote(filename)

        response.setdefault("Content-Disposition", "attachment;filename=" + filename)
        return response


@auth_session
@score_setting(action="评论资源")
def comment(request, res_id):
    # 获取 登录的用户ID
    user_id = db.get_current_user_id(request)

    param = request.POST.dict()
    param["user_id"] = user_id
    param["res_id"] = res_id

    # 直接将数据存储到表中
    sql = "insert into t_resource_comment(star, content, comment_time,user_id, res_id) values(" \
          " %(star)s , %(content)s, now(), %(user_id)s, %(res_id)s )"

    # 执行SQL ，并获取主键
    pk = db.update(sql, args=param)

    # 根据评论的 ID ，查询 评论的人，头像，时间，星级，和内容
    sql = "select t.*, f.nickname from t_resource_comment t left join t_user_info f on t.user_id = f.user_id where t.id =%s"

    # 获取评论信息
    comments = db.query_one(sql, args=(pk,))

    return JsonResponse(comments)
