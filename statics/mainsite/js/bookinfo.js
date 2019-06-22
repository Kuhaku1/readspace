function oklike() {
  //   console.log("oklike")
  sendmessage(likeurl, {
    "event": "ok",
    "bookid": bookid,
  }, handlelike)
}

function handlelike() {
  bookeventtag[0].classList.add("hide");
  bookeventtag[1].classList.remove("hide");
}

function oklikecancel() {
  //   console.log("oklikecancel")
  sendmessage(likeurl, {
    "event": "cancel",
    "bookid": bookid,
  }, handlelikecancel)
}

function handlelikecancel() {
  bookeventtag[1].classList.add("hide");
  bookeventtag[0].classList.remove("hide");
}

function oncollection() {
  //   console.log("collection")
  sendmessage(collectionurl, {
    "event": "ok",
    "bookid": bookid,
  }, handlecollection)
}

function handlecollection() {
  bookeventtag[2].classList.add("hide");
  bookeventtag[3].classList.remove("hide");
}


function oncollectioncancel() {
  //   console.log("collectioncancel")
  sendmessage(collectionurl, {
    "event": "cancel",
    "bookid": bookid,
  }, handlecollectioncancel)
}

function handlecollectioncancel() {
  bookeventtag[3].classList.add("hide");
  bookeventtag[2].classList.remove("hide");
}


function oncoin() {
  //   console.log("coin")
  sendmessage(coinurl, {
    "event": "ok",
    "bookid": bookid,
  }, handlcoin)
}

function handlcoin() {
  bookeventtag[4].classList.add("hide");
  bookeventtag[5].classList.remove("hide");
}

var bookeventtag = ""

function onsubmit() {
  var submittext = document.getElementById("submittext");
  sendmessage(commenturl, {
    "message": submittext.value,
    "bookid": bookid,
  }, function () {

  });
}


function main() {
  var bookevent = document.getElementById("bookevent")
  bookeventtag = bookevent.getElementsByTagName("span")
  if (islogin == "False") {
    return false;
  }
  bookeventtag[1].addEventListener("click", oklikecancel, false);
  bookeventtag[0].addEventListener("click", oklike, false);

  bookeventtag[3].addEventListener("click", oncollectioncancel, false);
  bookeventtag[2].addEventListener("click", oncollection, false);

  bookeventtag[4].addEventListener("click", oncoin, false);
  var submit = document.getElementById("submitcomment");
  submit.addEventListener("click", onsubmit, false);

  console.log(islogin)
}


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
        handlefunc()
      }
    },
    failure: function (response) {
      console.log(JSON.parse(response))
    }
  });
}
window.onload = main
