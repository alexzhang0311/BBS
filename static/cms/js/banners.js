//function包裹在$中代表整个网页加载完毕后才执行
$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var nameInput = $("input[name=input-filename]");
        var imageInput = $("input[name=input-picture]");
        var linkInput = $("input[name=input-link]");
        var priorityInput = $("input[name=input-weight]");

        var name = nameInput.val();
        var image = imageInput.val();
        var link = linkInput.val();
        var priority = priorityInput.val();
        var submitType = self.attr('data-type');
        var bannerID = self.attr('data-id');

        if(!name || !image || !link || !priority) {
            xtalert.alertToast('请输入完整的轮播图数据');
            return;
        }
        var url = '';
        if(submitType=='update'){
            url = '/cms/ubanner/';
        }else {
            url = '/cms/abanner/';
        }
        zlajax.post({
            "url":url,
            "data":{
                "name":name,
                "image_url":image,
                "link_url":link,
                "priority":priority,
                "banner_id":bannerID
            },
            "success":function (data) {
                dialog.modal("hide");
                // console.log(name);
                // console.log(image);
                // console.log(link);
                // console.log(priority);
                if(data['code'==200]){
                    window.location.reload(); //重新加载当前页面
                }else {
                    xtalert.alertInfo(data['message']);
                }
            },
            "fail":function () {
                xtalert.alertNetworkError();
            }
        });

    });
});


$(function () {
    $(".edit-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal('show');
        var tr = self.parent().parent(); //获取edit-banner-btn的爷爷节点，即tr
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        var nameInput = dialog.find("input[name=input-filename]");
        var imageInput = dialog.find("input[name=input-picture]");
        var linkInput = dialog.find("input[name=input-link]");
        var priorityInput = dialog.find("input[name=input-weight]");
        var saveBtn = dialog.find("#save-banner-btn");

        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        saveBtn.attr("data-type","update");
        saveBtn.attr("data-id",tr.attr('data-id'));

    })
})

$(function () {
    $(".del-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var bannerID = tr.attr('data-id');
        xtalert.alertConfirm({
            "msg":"确定删除该轮播图吗？",
            "confirmCallback":function () {
                zlajax.post({
                    "url":"/cms/dbanner/",
                    "data":{
                        "banner_id":bannerID
                    },
                    "success":function (data){
                        if(data['code'==200]){
                            xtalert.alertSuccess('删除成功');
                            window.location.reload();
                        }else {
                            xtalert.alertInfo(data['message']);
                        }
                    },
                    "fail":function (){
                        xtalert.alertNetworkError();
                    }
                })
            }
        });
    });
});