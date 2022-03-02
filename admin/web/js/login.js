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