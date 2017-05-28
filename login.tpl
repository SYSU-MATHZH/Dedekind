<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="initial-scale=1.0,user-scalable=no,maximum-scale=1,width=device-width">
    <title>Login</title>
    <style>
        * {
            box-sizing: border-box
        }
        .login{
            width: 340px;margin:0 auto;
            border:1px solid #beb19b;
            border-radius:3px;
            padding: 20px;
            font-family: "微软雅黑";font-size: 14px;
        }
        .form-body{
            padding: 10px;
        }
        label.text_label{
            display: block;
            margin-bottom: 7px;
        }
        input.text_box{
            margin-top:5px;
            margin-bottom: 15px;
            display: block;
            width: 100%;

            min-height: 34px;
            padding: 6px 8px;
            font-size: 14px;
            line-height: 20px;
            color: #24292e;
            vertical-align: middle;
            background-color: #fff;
            background-repeat: no-repeat;
            background-position: right 8px center;
            border: 1px solid #d1d5da;
            border-radius: 3px;
            outline: none;
            box-shadow: inset 0px 1px 2px rgba(27,31,35,0.075);
        }


        }

    </style>
</head>

<body>
    <div class="login">
    <form action="/login" method="POST">
        <label class="text_label" for="user_name">用户名</label>
        <input class="text_box"type="text" name="user_name"  >
        <label class="text_label" for="user_password">密码</label>
        <input class="text_box" type="password"  name="user_password" >
        <input type="checkbox" name="loginstatus">
        <label for="loginstatus">自动登录(5天内有效)</label>
        <p>
            <input type="submit" name="save" value="登录">
        </p>
    </form>
    </div>
</body>

</html>
