$(function () {
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
        var email = $("input[name=email]").val();
        if(!email){
            xtalert.alertInfoToast('请输入邮箱');
            return;
        }
        zlajax.get({
            'url':'/cms/email_captcha/',
            'data': {
                'email':email
            },
            'success':function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('验证码发送成功，请注意查收');
                }else{
                    var message = data['message'];
                    xtalert.alertInfo(message)
                }
            },
            'fail':function (error) {
                xtalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var emailD = $("input[name=email]");
        var email = emailD.val();
        var captchaD = $("input[name=captcha]");
        var captcha = captchaD.val();
        if(!email){
            xtalert.alertInfoToast('请输入邮箱');
            return;
        }
        if(!captcha){
            xtalert.alertInfoToast('请输入验证码')
            return;
        }
        zlajax.post({
            'url':'/cms/resetemail/',
            'data':{
                'email':email,
                'captcha':captcha
            },
            'success':function (data) {
                if(data['code']==200){
                    xtalert.alertSuccessToast('恭喜！邮箱修改成功');
                    emailD.val("");
                    captchaD.val("");
                }else{
                    var message=data['message'];
                    xtalert.alertInfo(message);
                }
            },
            'fail':function (error) {
                xtalert.alertNetworkError();
            }
        })
    })
})