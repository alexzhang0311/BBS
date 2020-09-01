$(function () {
    $(".highlight-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if(highlight){
            url = '/cms/unhpost/';
        }else {
            url = '/cms/hpost/';
        }
        zlajax.post({
            'url':url,
            'data':{
                'post_id':post_id
            },
            'success':function (data) {
                if(data['code']==200){
                    xtalert.alertSuccess('操作成功');
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else {
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail':function () {
                xtalert.alertNetworkError();
            }
        })
    });
});