// 1. Add type checking.
// 2. Improve Regex.
// 3. make pop-ups instead of alerts.

function login_input_check(){
    var userID = document.getElementById("userID").value;
    var inputPassword = document.getElementById("inputPassword").value;
    
    var check1 = checkUserID(userID);
    var check2 = checkPassword(inputPassword);
    return check1&check2;
}
function checkUserID(x){
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