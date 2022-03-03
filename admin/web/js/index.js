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

async function getstatus(){
    console.log('geting info')
    let data = await eel.status()()
    let table = document.getElementById('data')
    
    let tbod = ''
    for(i in data){
        data1 = data[i]
        text = '<tr>'
        for(j in data1){
            text += '<td>'+data1[j]+'</td>'
        }
        text+='</tr>'
        tbod += text

    }
    table.innerHTML = tbod
    console.log(data)
    
}