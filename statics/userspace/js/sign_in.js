function signchioce() {
  var listen = document.getElementById('SelectionMark');
  var selectmarkforli = listen.getElementsByTagName('li');
  var signInButton = document.getElementById('signInButton');
  // for (var i = 0; i < selectmarkforli.length; i++) {
  //     selectmarkforli[i].addEventListener('click', signinhandle, false);
  // }
  if (signflag) {
    selectmarkforli[parseInt(sign_in_li_index) - 1].addEventListener('click', signinhandle, false);
    signInButton.addEventListener('click', signinhandle, false);
  }
}

function signinhandle() {
  console.log(this.dataset.sign);
  sendajaxdata(this.dataset.sign);
}

window.onload = signchioce;

function sendajaxdata(sign) {
  ajax({
    method: 'GET',
    url: sign_inurl,
    data: {
      state: sign,
    },
    success: function (response) {
      var listen = document.getElementById('SelectionMark');
      var selectmarkforli = listen.getElementsByTagName('li');
      selectmarkforli[parseInt(sign_in_li_index) - 1].classList.remove('animationsign');
      selectmarkforli[parseInt(sign_in_li_index) - 1].removeEventListener('click', signinhandle, false);
      var signInButton = document.getElementById('signInButton');
      signInButton.classList.add('signInButtonfin');
      if (JSON.parse(response)['state'] == 'ok') {
        console.log('签到成功');
      } else {
        if (JSON.parse(response)['state'] == 'stop') {
          console.log('已经签过到了不要在重复了');
        }
      }
    },
    failure: function (tmp) {
      console.log('error');
    }
  });
}
