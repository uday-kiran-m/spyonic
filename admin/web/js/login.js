var reg = document.getElementById('register');
var login = document.getElementById('login')
function OpenRegister() {
    reg.style.display = 'block';
    login.style.display = 'none';

}
function Openlogin() {
    login.style.display = 'block';
    reg.style.display = 'none';
}
function trylogin(){
    console.log('logging')
    var email = document.getElementById('lemail')
    var passwd = document.getElementById('lpasswd')
    eel.login(email,passwd)(function isreg(stats){
        if (stats = 0){
            console.log('cant login')
        }
        else{
            console.log('loggedin')
        }
    })
    
}
function tryregistering(){
    console.log('registering')
    var email = document.getElementById('remail')
    var passwd = document.getElementById('rpasswd')
    eel.register(email,passwd)(function isreg(stats){
        if (stats = 0){
            console.log('cant login')
        }
        else{
            console.log('loggedin')
        }
    })
    
}
async function cheklogin(){
    console.log('checking log');
    let x = await eel.checklogin()();
    console.log(x);
    if(x==1){
        window.location.href = '/html/index.html'
    }
    
}

window.onload = cheklogin()
function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  let expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function checkCookie() {
  let user = getCookie("username");
  if (user != "") {
    alert("Welcome again " + user);
  } else {
    user = prompt("Please enter your name:", "");
    if (user != "" && user != null) {
      setCookie("username", user, 365);
    }
  }
}