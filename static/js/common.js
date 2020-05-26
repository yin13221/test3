$(document).ajaxError(function (event, jqxhr, settings, thrownError) {

    if (jqxhr.status == 318) { // 代表异步请求的资源没有进行登录

        data = jqxhr.responseJSON

        //获取要跳转的 地址 url
        url = data.url
        // 跳转到登录页面
        window.location.href = "/?url=" + encodeURI(url)
    }
});
