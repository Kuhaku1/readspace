var start = {x: 0, y: 0};
var end = {x: 0, y: 0};
var starttime;
var endtime;
var pageflag = 0;
var moveflag = 0;
var rotationchart;
var Intervalflag;

function startchart(event) {
    clearInterval(Intervalflag);
    start.x = event.touches[0].pageX;
    moveflag = pageflag;
    // pageflag = rotationchart.style.left;
    // if (!pageflag) {
    //     pageflag = 0;
    // } else {
    //     pageflag = parseInt(pageflag);
    // }
    starttime = new Date().getTime();
}

function endchart(event) {
    endtime = new Date().getTime();
    var viewindex;
    if (Math.abs(pageflag - moveflag) > 120) {
        var direction_rate = pageflag - moveflag > 0 ? -1 : 1;
        pageflag = pageflag + direction_rate * 375;
        viewindex = Math.floor(pageflag / 375) * -1;
        var rotationchartindex = document.getElementById('rotationchartindex');
        var rotationchartindexactivespan = rotationchartindex.getElementsByClassName('active');
        rotationchartindexactivespan[0].classList.remove('active');
        rotationchartindex.getElementsByTagName('span')[viewindex].classList.add('active');
    } else if (endtime - starttime < 200) {
        viewindex = Math.floor(pageflag / 375) * -1 + 1;
        atag = rotationchart.getElementsByTagName('a');
        atagindexelement = atag[viewindex];
        console.log('就不跳转到' + atagindexelement.href);
        Intervalflag = setInterval(rotationcharttimer, 2000);
        return true;
    }
    rotationchart.style.left = pageflag/16 + 'rem';
    Intervalflag = setInterval(rotationcharttimer, 2000);
}

function movechart(event) {
    end.x = event.touches[0].pageX;
    moveflag = pageflag + end.x - start.x;
    if (moveflag > 0) {
        moveflag = 0;
    } else if (moveflag < -1125) {
        moveflag = -1125;
    }
    rotationchart.style.left = moveflag/16 + 'rem';
}

function main() {
    rotationchart = document.getElementById('rotationchart');
    rotationchart.addEventListener("touchstart", startchart, true ? { passive: true }:false);
    rotationchart.addEventListener("touchmove", movechart, true ? { passive: true }:false);
    rotationchart.addEventListener("touchend", endchart, true ? { passive: true }:false);
    Intervalflag = setInterval(rotationcharttimer, 2000);
}

function rotationcharttimer() {
    rotationchart = document.getElementById('rotationchart');
    var viewindex = Math.floor(pageflag / 375) * -1;
    viewindex += 1;
    // console.log(viewindex);
    pageflag = 375 * viewindex * -1;
    var rotationchartindex = document.getElementById('rotationchartindex');
    var rotationchartindexactivespan = rotationchartindex.getElementsByClassName('active');
    rotationchartindexactivespan[0].classList.remove('active');
    rotationchart.style.left = pageflag/16 + 'rem';
    if (viewindex == 4) {
        viewindex = 0;
        pageflag = 0;
        setTimeout(reloadrotationchart, 305)
    }
    rotationchartindex.getElementsByTagName('span')[viewindex].classList.add('active');
}

function reloadrotationchart() {
    rotationchart.classList.remove('rotationcharttransition');
    rotationchart.style.left = 0 + 'rem';
    setTimeout(function () {
        rotationchart.classList.add('rotationcharttransition');

    }, 100)

}

window.onload = main;
