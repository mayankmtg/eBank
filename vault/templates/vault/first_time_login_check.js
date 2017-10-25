// 1. Add type checking.
// 2. Improve Regex.
// 3. make pop-ups instead of alerts.

function first_time_signin_check(){
    var inputEmail 				= document.getElementById("inputEmail").value;
    var inputOldPassword 		= document.getElementById("inputOldPassword").value;
    var inputNewPassword 		= document.getElementById("inputNewPassword").value;
    var inputRepeatNewPassword 	= document.getElementById("inputRepeatNewPassword").value;
    
    var check1 = checkUserName(inputEmail);
   	var check2 = checkPassword(inputOldPassword);
	var check3 = checkPassword(inputNewPassword);
	var check4 = checkPassword(inputRepeatNewPassword);
    return check1&check2&check3&check4;
}
function checkUserName(x){
    if (x == "") {                      // Empty String.
    	alert("Name must be filled out");
           return false;
    }
    return true;
}
function checkPassword(p){
  	if(p.length<8 || p.length>16){    // between given length.
    	alert("password should be between 8 and 16 characters long.");
    	return false;
    }
	// Idea send encrypted regex from server.
	// Work on regex.
    if(!new RegExp("([a-z]|[A-Z])").test(p)){    // Accept only good passwords satisfying the given regex.
        alert("passwd doesn't have alphabets.");
        return false;
    }
    return true;
}