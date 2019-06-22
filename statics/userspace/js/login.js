function form_submit(event) {
    // event.preventDefault();
    var username = document.getElementById('username');
    var error_info = document.getElementById('error_info');
    var userpassword = document.getElementById('userpassword');

    if (!username.value) {
        error_info.innerText = '用户名为空';
        error_info.classList.remove('hide');
        event.preventDefault();
        return false;
    } else {
        var patt = /^[a-zA-Z]\w*$/;
        if (username.value.length < 8 || !patt.test(username.value)) {
            error_info.innerText = '用户名格式错误';
            error_info.classList.remove('hide');
            event.preventDefault();
            return false;
        } else {
            var pawpatt = /\s/;
            if (pawpatt.test(userpassword.value) || userpassword.value.length < 8) {
                error_info.innerText = '密码格式错误';
                error_info.classList.remove('hide');
                event.preventDefault();
                return false;
            }
        }
    }
    return false;
}

function main() {
    form_id = document.getElementById('login_user');
    form_id.addEventListener('submit', form_submit, false);
}

window.onload = main;
