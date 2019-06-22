function onclicksearch() {
  var value = document.getElementById("search_value")
  datajson = {
    "bn": value.value
  }
  console.log(datajson)
  sendajaxdata(datajson)
}

function main() {
  var search = document.getElementById("search")
  search.addEventListener('click', onclicksearch, false)
}



function sendajaxdata(sign) {
  ajax({
    method: 'GET',
    url: searchurl,
    data: sign,
    success: function (response) {
      console.log(JSON.parse(response));
      searchresult = document.getElementById("searchresult");
      searchresult.innerHTML = "";
      result = JSON.parse(response)["result"]
      if (result.length > 0) {
        resultlist = new Array()
        for (var i = 0; i < result.length; i++) {
          bookindexurl = bookurl.replace(/0/g, result[i].id)
          iteemstr = "<a class=\"noshadow\" href=\"" + bookindexurl + "\"> \
          <li>\
            <img src=\"" + result[i].image + "\" alt=\"图片\">\
            <div class=\"search_result_info\">\
              <div>\
                <span>" + result[i].name + "</span>\
              </div>\
              <div>\
                <span>" + result[i].statedis + "</span><br>\
                <span>" + result[i].publicatioDay + "</span>\
              </div>\
            </div>\
          </li>\
        </a>"
          resultlist.push(iteemstr)
        }
        // console.log('签到成功');
        searchresult.innerHTML = resultlist.join("")
      } else {
        searchresult.innerHTML = "结果为空"
      }
    },
    failure: function (tmp) {
      console.log('error');
    }
  });
}


window.onload = main
