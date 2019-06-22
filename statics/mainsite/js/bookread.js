function function_menu() {
  consolemenu = document.getElementById("consolemenu");
  console.log("SSSSSS")
  console.log("SSSSSS")
  if (consolemenu.classList.contains('hide')) {
    consolemenu.classList.remove('hide');
  } else {
    consolemenu.classList.add('hide');
  }
}
var globalfontsign = 3;

function updatefontsizeshow() {
  contextfontsize = document.getElementById("contextfontsize");
  switch (globalfontsign) {
    case 2:
      contextfontsize.innerHTML = "小号"
      break;
    case 3:
      contextfontsize.innerHTML = "中号"
      break;
    case 4:
      contextfontsize.innerHTML = "大号"
  }
}


function enlargefontfunc(event) {
  if (globalfontsign < 4) {
    bookcontext = document.getElementById("bookcontext");
    bookcontext.classList.remove("bookcontextfont_" + globalfontsign);
    globalfontsign = globalfontsign + 1;
    bookcontext.classList.add("bookcontextfont_" + globalfontsign);
    updatefontsizeshow();
  }
  event.cancelBubble = true;
}

function narrowfontfunc(event) {
  if (globalfontsign > 2) {
    bookcontext = document.getElementById("bookcontext");
    bookcontext.classList.remove("bookcontextfont_" + globalfontsign);
    globalfontsign = globalfontsign - 1;
    bookcontext.classList.add("bookcontextfont_" + globalfontsign);
    updatefontsizeshow();
  }
  event.cancelBubble = true;
}

function main() {
  bookmain = document.getElementById("bookmain");
  enlargefont = document.getElementById("enlargefont");
  narrowfont = document.getElementById("narrowfont");


  bookmain.addEventListener("click", function_menu, false);
  enlargefont.addEventListener("click", enlargefontfunc, false);
  narrowfont.addEventListener("click", narrowfontfunc, false);


  setInterval(() => {
    sendmessage("/api/readtimehandle", {
        "event": "ok",
        "bookid": bookid,
      },
      null)
  }, 5000);
}
window.onload = main;



function sendmessage(url, message, handlefunc) {
  console.log(url);
  console.log(message);
  var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0];
  message["csrfmiddlewaretoken"] = csrfmiddlewaretoken.value;
  console.log(message)
  ajax({
    method: 'POST',
    url: url,
    data: message,
    success: function (response) {
      var resutl = JSON.parse(response);
      if (resutl["state"] == "ok") {
        // handlefunc()
        console.log("签到心跳once")
      }
    },
    failure: function (response) {
      console.log(JSON.parse(response))
    }
  });
}
