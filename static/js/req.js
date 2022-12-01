
function RequestPost(url, json) {
    var data;
    $.ajax({
      url: url,
      async: false, 
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
        loading(_this)
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
    var _html = RequestPost('/eventhtml', {'type':1})
    var parent = _this.parentElement;
    _this.remove()
    parent.innerHTML += _html; 
}


function openRegister(_this){
     loading(_this)
    // ajax to get html from server 
    var _html = RequestPost("/eventhtml", {"type": 2})
    var parent = _this.parentElement;
    // remove button
    _this.remove();
    // append html
    parent.innerHTML += _html;
}

function openRegisterLvl1(_this){
    // get values from inputs 
    parent = _this.parentElement
    parent2 = parent.parentElement
    // loading
    loading(_this);
    // ajax request: json, post
    $.ajax({
      url: "/register_event",
      type: 'POST',
      data:{'name': parent.children[0x0].value,
            'phone': parent.children[0x2].value,
            'id': parent.children[0x4].value,
            'lvl':1},
      success: function (res) {
        if (res.success){
            // clear parent from element
            parent2.innerHTML = "";
            // request
            var _html = RequestPost("/eventhtml", {"type": 3});
            parent2.innerHTML += _html;

        }
        else{
            alert("אחד הפרטים או יותר שגוי");
            unloading(_this, "המשך");
        }
      }
    });
    
    
}
function openRegisterLvl2(parent){
    $(parent).fadeOut(500);
    // async callback
    // setTimeout(()=>{ parent.innerHTML="";$(parent).fadeIn(1)}, 500)
    parent.innerHTML="";
    $.ajax({
        url:"/register_event",
        type:"POST",
        data:null
    })  

}


function loading(_this){
    _this.children[0].remove();
    cntr = document.createElement("center");
    dv = document.createElement("div");
    dv.className = "loading";
    cntr.append(dv);
    _this.appendChild(cntr);
}


function unloading(_this, text){
    _this.children[0].remove();
    span = document.createElement("span");
    span.innerText = text
    _this.appendChild(span);
}

