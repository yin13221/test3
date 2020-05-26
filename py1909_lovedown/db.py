from django.db import connection as conn


def update(sql, args=None):
    """
    该方法支持增删改 三种操作
    :param sql:
    :param args:
    :return:
    """
    # 获取游标
    with conn.cursor() as cursor:
        cursor.execute(sql, params=args)
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount


def query_one(sql, args=None):
    """
    该方法查询单条记录
    :param sql:
    :param args:
    :return:
    """
    with conn.cursor() as cursor:
        cursor.execute(sql, params=args)
        # 获取查询结果
        res = cursor.fetchone()

        if res is None:
            return None

        columns = [t[0] for t in cursor.description]

        return dict(zip(columns, res))


def query_list(sql, args=None):
    """
    该方法查询多条记录
    :param sql:
    :param args:
    :return:
    """
    with conn.cursor() as cursor:
        cursor.execute(sql, params=args)
        # 获取查询结果
        res = cursor.fetchall()

        if res is None:
            return None
        columns = [t[0] for t in cursor.description]

        return [dict(zip(columns, r)) for r in res]


def query_proc_one(procedure_name, args=None):
    """
    该方法查询单条记录
    :param sql:
    :param args:
    :return: 返回一个字典
    """
    with conn.cursor() as cursor:
        cursor.callproc(procedure_name, params=args)
        # 获取查询结果
        res = cursor.fetchone()
        if res is None:
            return None

        columns = [t[0] for t in cursor.description]
        return dict(zip(columns, res))


def get_current_user_id(request):
    user = request.session.get("LOGIN_LOCAL_FLAG")
    if user is None:
        return None
    return user.get("id")
