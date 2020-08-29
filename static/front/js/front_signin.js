$(function () {
    $("#submmit").click(function (event) {
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var password_input = $("input[name='password']");
        var remember_input = $("input[name='remember']");

        var telephone = telephone_input.val();
        var password = password_input.val();
        var remember = remember_input.is(':checked')
        // var remember = remember_input.checked ? 1:0
        // var remember = remember_input.checked ? 1 : 0;//选择了为1，否则为0

        zlajax.post({
            'url':'/front/signin/',
            'data':{
                'telephone':telephone,
                'password':password,
                'remember': remember
            },
            'success':function (data) {
                if(data['code']==200){
                    var return_to = $("#return-to-span").text();
                    if (return_to){
                        window.location = return_to;
                    }else {
                        window.location = '/front/';
                    }
                }else {
                    xtalert.alertInfo(data['message'])
                }
            },
            'fail':function (data) {
                xtalert.alertNetworkError()
            }
        })
    });
});