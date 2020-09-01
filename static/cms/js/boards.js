$(function () {
    $("#add-board-btn").click(function (event) {
        event.preventDefault();
        xtalert.alertOneInput({
            'text':'请输入板块名称',
            'placeholder':'板块名称',
            'confirmCallback':function (inputValue) {
                zlajax.post({
                    'url':'/cms/aboard/',
                    'data':{
                        'name':inputValue
                    },
                    'success':function (data) {
                        if (data['code']==200){
                            // window.location.reload();
                            xtalert.alertSuccess('板块添加成功')
                        }else {
                            xtalert.alertInfo(data['message'])
                        }
                    }
                });
            }
        });
    });
});

$(function () {
    $(".edit-board-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('board-name');
        var id = tr.attr('board-id');

        xtalert.alertOneInput({
                'text':'请输入板块名称',
                'placeholder':'板块名称',
                'confirmCallback':function (inputValue) {
                    zlajax.post({
                        'url':'/cms/uboard/',
                        'data': {
                            'board_id':id,
                            'name':inputValue
                        },
                        'success':function (data) {
                            if(data['code']==200){
                                window.location.reload();
                                xtalert.alertSuccess('板块更新成功')
                            }else{
                                xtalert.alertInfo(data['message'])
                            }
                        },
                        'fail':function () {
                            xtalert.alertNetworkError()
                        }
                    });
                }
        }
        )
    });
});

$(function () {
    $(".del-board-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var id = tr.attr('board-id')
        xtalert.alertConfirm({
            'msg':'确定删除该板块？',
            'confirmCallback':function () {
                zlajax.post({
                    'url':'/cms/dboard/',
                    'data':{
                        'board_id':id
                    },
                    'success':function (data) {
                        if(data['code']==200){
                            window.location.reload();
                            xtalert.alertSuccess('板块删除成功')
                        }else {
                            xtalert.alertInfo(data['message'])
                        }
                    },
                    'fail':function () {
                        xtalert.alertNetworkError()
                    }
                });
            }
        });
    });
});