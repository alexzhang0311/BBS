$(function () {
    var ue = UE.getEditor("editor",{
        'serverUrl':'/ueditor/upload/',
        'toolbars': [
            [
                'bold', //加粗
                'italic', //斜体
                'underline', //下划线
                'subscript', //下标
                'superscript', //上标
                'horizontal', //分隔线
                'fontfamily', //字体
                'fontsize', //字号
                'link', //超链接
                'emotion', //表情
                'forecolor', //字体颜色
                'imagenone', //默认
                'imageleft', //左浮动
                'imageright', //右浮动
                'imagecenter', //居中
            ]
        ]
    });
    window.ue = ue;
});

$(function () {
    $("#comment-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            window.location = '/front/signin/';
        }else {
            var content = window.ue.getContent();
            var post_id = $("#post-content").attr('data-id');
            zlajax.post({
                'url':'/front/acomment/',
                'data':{
                    'content':content,
                    'post_id':post_id
                },
                'success':function (data) {
                    if(data['code']==200){
                        xtalert.alertSuccess('评论添加成功！');
                        window.location.reload();
                    }else {
                        xtalert.alertInfo(data['message']);
                    }
                },
                'fail':function (error) {
                    xtalert.alertNetworkError();
                }
            });
        }
    });
});