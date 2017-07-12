function go_index() {
    get_user_id();
    get_notice();
}

function get_user_id() { //从数据库获取JSON数据
    xmlHttp1 = createXMLHttpRequest();
    var url = "user_info?user_id=" + getCookie("user_id_public");
    xmlHttp1.open("GET", url, true); // 异步处理返回
    xmlHttp1.onreadystatechange = callback1;
    xmlHttp1.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;");
    xmlHttp1.send();
}

function createXMLHttpRequest() { //与python响应获取信息
    var xmlHttp;
    if (window.XMLHttpRequest) {
        xmlHttp = new XMLHttpRequest();
        if (xmlHttp.overrideMimeType)
            xmlHttp.overrideMimeType('text/xml');
    } else if (window.ActiveXObject) {
        try {
            xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            try {
                xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (e) {}
        }
    }
    return xmlHttp;
}

function callback1() {
    if (xmlHttp1.readyState  ==  4  &&  xmlHttp1.status  ==  200) //判断返回码
    {
        var data = JSON.parse(xmlHttp1.responseText);
        //alert(data.user_info.name) ;//显示数据库的成员姓名
        user_name.innerHTML = data.user_info.name; //在body里面直接显示出姓名
        user_id.innerHTML = data.user_info.code; //同上
        user_suahours.innerHTML = data.user_info.suahours; //公益时信息
    }
}

function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
    if (arr = document.cookie.match(reg))
        return unescape(arr[2]);
    else
        return null;
}

function get_notice() { //从数据库获取JSON数据
    xmlHttp = createXMLHttpRequest();
    var url = "notice";
    xmlHttp.open("GET", url, true); // 异步处理返回
    xmlHttp.onreadystatechange = callback2;
    xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;");
    xmlHttp.send();
}

function callback2() {
    if (xmlHttp.readyState  ==  4  &&  xmlHttp.status  ==  200) //判断返回码
    {
        var data = JSON.parse(xmlHttp.responseText);
        //alert(data.user_info.name) ;//显示数据库的成员姓名
        user_GSUA_title.innerHTML = data.notices[1].notice_title; //if check == 0 输出
        //a=document.createElement("label"); 创建动态label  b= document.createTextNode("aaa");  定义label的值b
        //a.appendChild(b);为a赋予b的值  document.body.appendChild(a); 创建一个新的label
        user_notice_detail.innerHTML = data.notices[1].notice_details;
        user_GSUA_time.innerHTML = data.notices[1].time;
        user_actorGroupid.innerHTML = data.notices[1].actorGroup_id;
    }
}
