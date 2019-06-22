function f() {
  var screenitems = document.getElementById('screenitem');
  var screenitem = screenitems.getElementsByTagName('span');
  for (var i = 0; i < screenitem.length - 1; i++) {
    screenitem[i].addEventListener('click', qw, false);
  }

  var deltailsitem = document.getElementById('screen1');
  var itemli = deltailsitem.getElementsByTagName('li');
  for (var i = 0; i < itemli.length; i++) {
    itemli[i].getElementsByTagName("a")[0].addEventListener('click', clickfuncscreen1, false);
  }

  var deltailsitem = document.getElementById('screen2');
  var itemli = deltailsitem.getElementsByTagName('li');
  for (var i = 0; i < itemli.length; i++) {
    itemli[i].getElementsByTagName("a")[0].addEventListener('click', clickfuncscreen2, false);
  }

  var deltailsitem = document.getElementById('screen3');
  var itemli = deltailsitem.getElementsByTagName('li');
  for (var i = 0; i < itemli.length; i++) {
    itemli[i].getElementsByTagName("a")[0].addEventListener('click', clickfuncscreen3, false);
  }

  screenitem[3].addEventListener('click', onclickok, false);
}

function qw() {
  var tmp = document.getElementById('deltails_item');
  var deltailsitem = tmp.getElementsByTagName('div');
  if (!deltailsitem[parseInt(this.dataset.identity)].classList.contains('hide')) {
    // deltailsitem[parseInt(this.dataset.identity)].classList.add('hide');
    var ind = parseInt(this.dataset.identity);
    tmp.style.height = '0';

    setTimeout(function () {
      deltailsitem[ind].classList.add('hide');
    }, 100);
  } else {
    for (var i = 0; i < deltailsitem.length; i++) {
      if (!deltailsitem[i].classList.contains('hide')) {
        deltailsitem[i].classList.add('hide');
        break;
      }
    }
    deltailsitem[parseInt(this.dataset.identity)].classList.remove('hide');
    tmp.style.height = deltailsitem[parseInt(this.dataset.identity)].scrollHeight + 'px'
  }
}

function clickfuncscreen1() {
  var screenitems = document.getElementById('screenitem');
  var screenitem = screenitems.getElementsByTagName('span');
  screenitem[0].innerText = this.innerText;

  var tmp = document.getElementById('deltails_item');
  var deltailsitem = tmp.getElementsByTagName('div');
  tmp.style.height = '0';

  setTimeout(function () {
    deltailsitem[0].classList.add('hide');
  }, 100);
}

function clickfuncscreen2() {
  var screenitems = document.getElementById('screenitem');
  var screenitem = screenitems.getElementsByTagName('span');
  screenitem[1].innerText = this.innerText

  var tmp = document.getElementById('deltails_item');
  var deltailsitem = tmp.getElementsByTagName('div');
  tmp.style.height = '0';

  setTimeout(function () {
    deltailsitem[1].classList.add('hide');
  }, 100);

}

function clickfuncscreen3() {
  var screenitems = document.getElementById('screenitem');
  var screenitem = screenitems.getElementsByTagName('span');
  screenitem[2].innerText = this.innerText;

  var tmp = document.getElementById('deltails_item');
  var deltailsitem = tmp.getElementsByTagName('div');
  tmp.style.height = '0';

  setTimeout(function () {
    deltailsitem[2].classList.add('hide');
  }, 100);

}

function onclickok() {
  var screenitems = document.getElementById('screenitem');
  var screenitem = screenitems.getElementsByTagName('span');
  var screen0 = ''
  var screen1 = ''
  var screen2 = ''
  if (screenitem[0].innerText == "付费") {
    screen0 = "全部";
  } else {
    screen0 = screenitem[0].innerText;
  }

  if (screenitem[1].innerText == "类型") {
    screen1 = "全部";
  } else {
    screen1 = screenitem[1].innerText;
  }
  if (screenitem[2].innerText == "状态") {
    screen2 = "全部";
  } else {
    screen2 = screenitem[2].innerText;
  }

  datajson = {
    "v1": screen0,
    "family": screen1,
    "state": screen2,
  }
  console.log(datajson);
  sendajaxdata(datajson);
}

window.onload = f;

function sendajaxdata(sign) {
  ajax({
    method: 'POST',
    url: finurl,
    data: sign,
    success: function (response) {
      console.log(JSON.parse(response));
      findresult = document.getElementById("findresult");
      findresult.innerHTML = "";
      result = JSON.parse(response)["result"]
      if (result.length > 0) {
        resultlist = new Array()
        for (var i = 0; i < result.length; i++) {

          if (!result[i].lastUpdated)
            lastUpdated = "没有数据";
          else
            lastUpdated = result[i].lastUpdated;
          iteemstr = "<a class=\"noshadow\" href=\"" + result[i].idurl + "\">\
<li class=\"info_item fl\">\
<img src=\"" + result[i].image + "\" alt=\"" + result[i].name + "\">\
<span class = \"item_name\" > " + result[i].name + "\"</span> \
<span class = \"item_result\" > " + lastUpdated + " </span> \
</li > \
</a>"
          resultlist.push(iteemstr)
        }
        // console.log('签到成功');
        findresult.innerHTML = resultlist.join("")
      } else {
        findresult.innerHTML = "没有数据"
      }
    },
    failure: function (tmp) {
      console.log('error');
    }
  });
}
