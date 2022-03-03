// eel.expose(sidebar)
function sidebar(){
    var headnav = document.getElementById("header")
    var headnavwidth = window.getComputedStyle(headnav)
    var main = document.getElementById("main")
    var menu_icon = document.getElementById("menu-icon")
    if ((headnavwidth.width == "0px" && headnav.style.width == "")||(headnav.style.width=='0px')){
        headnav.style.width = "200px"
        main.style.marginLeft = '200px'
        menu_icon.innerHTML= '&#10005;'
    }
    else{
        headnav.style.width = "0px"
        main.style.marginLeft = '0px'
        menu_icon.innerHTML = '&#9776;'
    }
}

window.onload = async function(){
    console.log('geting info')
    let data = await eel.status()
    let p = document.getElementById('data')
    p.innerHTML = data
}