/* show password */
const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');

togglePassword.addEventListener('click', function (e) {
  // toggle the type attribute
  const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
  password.setAttribute('type', type);
  // toggle the eye / eye slash icon
  this.classList.toggle('bi-eye');
});

function varify_password() {  
  var pw1 = document.getElementById("password").value;  
  var pw2 = document.getElementById("repass").value;
 
// check empty password field  
  if(pw1 == "") {  
     document.getElementById("message").innerHTML = "*Fill the password please!";  
     return false;  
  }  
   
// minimum password length validation  
  if(pw1.length < 8) {  
     document.getElementById("message").innerHTML = "*Password length must be at least 8 characters";  
     return false;  
  }
  
  var correct = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
  if(!pw1.match(correct)){
    document.getElementById("message").innerHTML = "*Password should contain at least one digit, one lower case, one upper case";  
    return false;
  }

  //clear messages
  document.getElementById("message").innerHTML = "";  

  if(pw1 != pw2){  
    document.getElementById("message_re").innerHTML = "*Passwords did not match";  
    return false;
  }

  document.getElementById("message_re").innerHTML = "";  
  return true; 

} // varify_password

/*function match_password() {  
  var pw1 = document.getElementById("password");  
  var pw2 = document.getElementById("repass");  
  if(pw1 != pw2)  
    document.getElementById("message_re").innerHTML = "*Passwords did not match";  
 } */ 



