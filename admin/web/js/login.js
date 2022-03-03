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
async function trylogin(){
    console.log('logging')
    var email = document.getElementById('lemail')
    var passwd = document.getElementById('lpasswd')
    eel.login(email,passwd)(function isreg(stats){
        if (stats = 1){
            console.log('logged in')
            setCookie("username", email);
            setCookie("login",1);

        }
        else{
            console.log(stats)
        }
    })
    
}
async function tryregistering(){
    console.log('registering')
    var email = document.getElementById('remail')
    var passwd = document.getElementById('rpasswd')
    eel.register(email,passwd)(function isreg(stats){
        if (stats = 1){
            console.log('registered')
            setCookie("username", email);
            setCookie("login",1);
        }
        else{
            console.log(stats)
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



function setCookie(cname, cvalue) {
  document.cookie = cname + "=" + cvalue + ";" ;
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
  let status = getCookie("login")
  console.log('checking cookie')
  if (user != "" || status != 0) {
    // alert("Welcome again " + user);
    console.log('authenticating')
    cheklogin()
  } else {
    // user = prompt("Please enter your name:", "");
    if (user != "" && user != null) {
      console.log('user login required')
      setCookie("username", user);
      setCookie("login",0);
      Openlogin()
    }
    else{
        console.log('user unknown')
        setCookie("username",'')
        OpenRegister()
    }
  }
}


window.onload = checkCookie()