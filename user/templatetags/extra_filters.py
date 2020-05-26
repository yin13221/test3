from django.template.defaultfilters import register

ext_list = ["doc", "docx", "exe", "pdf", "ppt", "rar", "txt", "xlsx", "zip"]


@register.filter(is_safe=True)
def sex(value):
    if value == "m":
        return "男"
    if value == "w":
        return "女"


@register.filter(is_safe=True)
def ext(value):
    return value if value in ext_list else "unknow"
