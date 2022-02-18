
console.log("signin")
/* show password */
  const togglePassword = document.querySelector('#togglePassword');
  const password = document.querySelector('#password_signup');

  togglePassword.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye / eye slash icon
    this.classList.toggle('fas fa-eye');
  });


function varify_signup(){
  if (varify_username() && varify_email() && varify_phone() && varify_password()){
    return true;
  }
  return false;
}//varify_signup

function varify_contactus(){
  if(varify_email() && varify_text(("subject", "subject_mes", "Subject cannot be blank")) && varify_text(("description", "description_mes", "Description cannot be blank"))) {
    return true;
  }
  return false;
}//varify_signup

function varify_donation() {
  if(varify_text("category", "category_mes", "Category cannot be blank") && varify_text("product", "product_mes", "Product cannot be blank") && varify_date_time() && varify_address()){
    return true
  }
  return false;
 } //varify_donation

function varify_username() {
  var user = document.getElementById("user_signup").value;
  if(user == ""){
    document.getElementById("username_mes").innerHTML = "Must enter a valid user name";
    return false;
  }
  document.getElementById("username_mes").innerHTML = "";  //clear messages
  return true;
} //varify_username

function varify_email() {
  var email_format = "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$";
  var email = document.getElementById("Email").value;
  if(!email.match(email_format)){
    document.getElementById("email_mes").innerHTML = "Must enter a valid email";
    return false;
  }
  document.getElementById("email_mes").innerHTML = "";  //clear messages
  return true;
} // varify_email

function varify_phone() {
  var phone_format = "[0][5][0-9]{1}[0-9]{3}[0-9]{4}"
  var phone = document.getElementById("phone").value;
  if(!phone.match(phone_format)){
    document.getElementById("phone_mes").innerHTML = "Must enter a valid phone";
    return false;
  }
  document.getElementById("phone_mes").innerHTML = "";  //clear messages
  return true;
} //varify_phone

function varify_password() {
  var pw1 = document.getElementById("password_signup").value;
  var pw2 = document.getElementById("repass_signup").value;

// check empty password field
  if(pw1 == "") {
     document.getElementById("password_mes").innerHTML = "Must enter a valid password";
     return false;
  }

// minimum password length validation
  if(pw1.length < 8) {
     document.getElementById("password_mes").innerHTML = "Password length must be at least 8 characters";
     return false;
  }

  var correct = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
  if(!pw1.match(correct)){
    document.getElementById("password_mes").innerHTML = "Password should contain at least one digit, one lower case, one upper case";
    return false;
  }

  document.getElementById("password_mes").innerHTML = ""; //clear password messages

  // check if passwords are matching
  if(pw1 != pw2){
    document.getElementById("repass_mes").innerHTML = "Passwords did not match";
    return false;
  }

  document.getElementById("repass_mes").innerHTML = "";  //clear repassword messages
  return true;

} // varify_password

// reset signin form
var inputs_signin = ["user_signin", "password"];
var j = 0 ;
function reset_signin(){
  var variable = document.getElementById(inputs_signin[i]);
  if (variable != null){
    document.getElementById(inputs_signin[i]).value = "";
  }
  if(i < inputs_signin.length){
    i++;
    reset_signin();
  }
  else {
    j = 0;
    document.getElementById("check").checked = true;
  }
}//reset_signin

// reset signup form
var inputs_signup = ["user_signup", "Email", "phone", "password_signup", "repass_signup"];
var i = 0 ;
function reset_signup(){
  var variable = document.getElementById(inputs_signup[i]);
  if (variable != null){
    document.getElementById(inputs_signup[i]).value = "";
  }
  if(i < inputs_signup.length){
    i++;
    reset_signup();
  }
  else {
    i = 0;
  }
}//reset_signup

function varify_text(id, mes_id, mes){
  var text = document.getElementById(id).value;
  if(text == ""){
    document.getElementById(mes_id).innerHTML = mes;
    return false;
  }
  document.getElementById(mes_id).innerHTML = "";  //clear messages
  return true;
}//varify_text

function varify_address(){
  var street =  document.getElementById("street").value;
  var number =  document.getElementById("number").value;
  var city =  document.getElementById("city").value;
  if (street != "" && number != "" && city != ""){
    document.getElementById("address_mes").innerHTML = "";  //clear messages
    return true;
  }
  else {
    document.getElementById("address_mes").innerHTML = "Address cannot be blank";
  }
} //varify_address

function varify_date_time() {
  var date = document.getElementById("avail_date").value;
  var time = document.getElementById("avail_time").value;
  if (date != "" && time != ""){
    document.getElementById("avail_mes").innerHTML = "";  //clear messages
    return true;
  }
  else {
    document.getElementById("avail_mes").innerHTML = "date or time cannot be blank";
  }
}