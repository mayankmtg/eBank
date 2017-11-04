function validateEmail(email){
    // alert(email);
    var reg = /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
    if(reg.test(email)){
        return true;
    }
    alert("Not a valid email address.");
    return false;
}

function validateName(username){
    var userRegex = new RegExp('^[a-zA-Z]*',"g");
    if(username.match(userRegex)){
        return true;
    }
    alert("Invalid Username.");
    return false;
}

function registerCheck(){
    var firstName       = document.getElementById("first_name").value;
    firstName=escapeHTMLEntityEndcoding(firstName);
    var lastName   = document.getElementById("last_name").value;
    lastName=escapeHTMLEntityEndcoding(lastName);
    var email    = document.getElementById("email").value;
    email=escapeHTMLEntityEndcoding(email);
    var check1  = validateEmail(email);
    var check2  = validateName(firstName);
    var check3  = validateName(lastName);
    return check1&check2&check3;
}

var button=document.getElementById("but");
button.addEventListener("click", function(event){
    if(!registerCheck()){
        event.preventDefault();
    }
});

function escapeHTMLEntityEndcoding(str){
    var ESC_MAP = {
        '&': '&amp;'    ,
        '<': '&lt;'     ,
        '>': '&gt;'     ,
        '"': '&quot;'   ,
        "'": '&#x27;'   ,
        '/': '&#x2F;'
    };
    for(var key in ESC_MAP){
        var regex = new RegExp(key,"g");
        if(ESC_MAP.hasOwnProperty(key)){
            str.replace(regex,ESC_MAP[key]);
        }
    }
    return str;
}
