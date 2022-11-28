
function RequestPost(json) {
    var data;
    $.ajax({
      url: "/events",
      async: false, 
      //very important: else php_data will be returned even before we get Json from the url
      type: 'POST',
      data:json,
      success: function (res) {
        data = res;
      }
    });
    return data;
}


var x = 0;
function enterToEvent(_this){
    /* UI */
    if (!x){
        
        console.log(_this.name);
        _this.children[0].remove();
        cntr = document.createElement("center");
        dv = document.createElement("div");
        dv.className = "loading";
        cntr.append(dv);
        _this.appendChild(cntr);
        x=1;
    }
    $.ajax({
        url:"/events",
        type:"POST",
        data:{name:_this.name},
        success:function(res){
            if (res.success){
                document.location = res.page;
            }
            else{
                x = 0
                _this.children[0].remove();
                sp = document.createElement("span");
                sp.textContent = "להשתתפות"
                _this.appendChild(sp)
            }
        }
    })       

}

function timerEvent(ctime){
    /* interval to countdown */
    var countdown = new Date(ctime).getTime();
    var TIMER = setInterval(function(){
        var ctime_now = new Date().getTime();
        var distance = countdown - ctime_now;
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        if (distance < 0) {
            clearInterval(TIMER);
            console.log("EXPIRED");
            days = "00";
            hours = "00";
            minutes = "00";
            seconds = "00";
        }
        document.getElementById("days").innerText = days;
        document.getElementById("hours").innerText = hours;
        document.getElementById("minutes").innerText = minutes;
        document.getElementById("second").innerText = seconds;

    }, 1000)

}

function loadTimer(n_event){
    $.ajax({
        url: "/timer_event",
        data:{event:n_event},
        type: "POST",
        success:(res) =>{
            if (res.success){
                timerEvent(res.event_time);
                setTitle(res.title_event)
            }
            else{
                console.log(res)
            }
        }
    })
}

function deleteBefore(){
    $("#second").addClass("no-after")
}

function setTitle(title){
    var x = document.getElementsByClassName("cal-title");
    x[0].innerText = title;
    // console.log(title);
}

function openEventData(_this){
    var _html = "<br><br><br><br><h1>hello></h1>"
    _this.remove()
}


function openRegister(_this){
    // ajax to get html from server 
    var _html = "<h1>hello</h1>";
    var parent = _this.parentElement;
    // remove button
    _this.remove();
    // append html
    parent.innerHTML += _html;
}