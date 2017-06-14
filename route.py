import sqlite3
import bottle
from beaker.middleware import SessionMiddleware
from paste import httpserver

SECRETKEY = 'rbbb=====afdasdasd'
DOMAIN = '0.0.0.0'


def login_check(session):
    user_id = session.get('user_id', -1)
    group_rank = session.get('group_rank', -1)
    user_id_cookie = bottle.request.get_cookie('user_id', secret=SECRETKEY)
    group_rank_cookie = bottle.request.get_cookie('group_rank', secret=SECRETKEY)
    print(user_id_cookie)
    if user_id_cookie is None:
        session['user_id'] = -1
        session['group_rank'] = -1
        bottle.response.delete_cookie('user_id_public')
        return False
    else:
        if user_id == -1 or user_id != user_id_cookie:
            session['user_id'] = user_id_cookie
            user_id = user_id_cookie
        if group_rank == -1 or group_rank != group_rank_cookie:
            session['group_rank'] = group_rank_cookie
        bottle.response.set_cookie('user_id_public', str(user_id))
        return True


@bottle.route('/')
def index():
    s = bottle.request.environ.get('beaker.session')
    if login_check(s):
        conn = sqlite3.connect('db_dedekind.db')
        user_id = s['user_id']
        c = conn.cursor()
        c.execute('''
            SELECT user_code, user_name, user_suahours, user_email
            FROM Users
            WHERE user_id = :user_id''', {'user_id': int(user_id)})
        result = c.fetchone()
        code, name, suahours, email = result
        return bottle.template('index.html')
    else:
        bottle.redirect('/login')


# 登录
@bottle.route('/login')
def login():
    s = bottle.request.environ.get('beaker.session')
    if login_check(s):
        bottle.redirect('/')
    else:
        return bottle.template('login.html')


@bottle.route('/img/<filename:re:.*\.png>')
def img_static(filename):
    return bottle.static_file(filename, root='./img')


@bottle.route('/login', method='POST')
def do_login():
    username = bottle.request.forms.get('user_name')
    password = bottle.request.forms.get('user_password')
    isSaveStatus = bottle.request.forms.get('loginstatus')
    conn = sqlite3.connect('db_dedekind.db')
    cur = conn.cursor()
    cur.execute('''SELECT user_id, user_password, group_rank
                    FROM Users JOIN Groups
                    ON user_code = :user_code AND Users.group_id = Groups.group_id''',
                {'user_code': username})
    result = cur.fetchone()
    if result is not None:
        user_id, user_password, group_rank = result
        if password == str(user_password):
            s = bottle.request.environ.get('beaker.session')
            s['user_id'] = int(user_id)
            if isSaveStatus:
                bottle.response.set_cookie(
                    'user_id', int(user_id), secret=SECRETKEY,
                    max_age=5 * 24 * 3600, path='/')
                bottle.response.set_cookie(
                    'group_rank', int(group_rank), secret=SECRETKEY,
                    max_age=5 * 24 * 3600, path='/')
            else:
                bottle.response.set_cookie(
                    'user_id', int(user_id), secret=SECRETKEY, path='/')
                bottle.response.set_cookie(
                    'group_rank', int(group_rank), secret=SECRETKEY, path='/')
            bottle.response.set_cookie(
                'login_status', 0, secret=SECRETKEY, path='/')
            # 0 means login successfully.

        else:
            conn.close()
            bottle.response.set_cookie(
                'login_status', 2, secret=SECRETKEY,
                path='/')
            # 2 means wrong password.
            bottle.redirect('/login')
    else:
        conn.close()
        bottle.response.set_cookie(
            'login_status', 1, secret=SECRETKEY, path='/')
        # 1 means wrong username
        bottle.redirect('/login')

    conn.close()
    bottle.redirect('/')


@bottle.route('/logout')
def logout():
    s = bottle.request.environ.get('beaker.session')
    if login_check(s):
        s['user_id'] = -1
        bottle.response.delete_cookie('user_id', secret=SECRETKEY)
    bottle.response.delete_cookie('login_status', secret=SECRETKEY)
    bottle.response.delete_cookie('group_rank', secret=SECRETKEY)
    bottle.response.delete_cookie('user_id_public')
    bottle.redirect('/')


# 用户信息
@bottle.route('/user_info')
def user_info():
    s = bottle.request.environ.get('beaker.session')
    json = {}
    user_id = bottle.request.query.user_id
    if login_check(s) and user_id is not '' and int(user_id) == s['user_id']:
        json['login_check'] = 0
        json['user_id'] = int(user_id)
        conn = sqlite3.connect('db_dedekind.db')
        c = conn.cursor()
        c.execute('''
            SELECT user_code, user_name, user_suahours, user_email, group_name, group_rank
            FROM Groups JOIN Users
            ON Groups.group_id = Users.group_id AND user_id = :user_id''',
                  {'user_id': int(user_id)})
        result = c.fetchone()
        info = {}
        info['code'], info['name'], info['suahours'], info[
            'email'], info['group'], info['rank'] = result
        json['user_info'] = info
        return json
    else:
        json['login_check'] = 1
        json['user_id'] = None
        json['user_info'] = {}
        return json


@bottle.route('/test')
def test():
    return bottle.template('test')


session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './tmp',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)
# bottle.run(app=app, host=DOMAIN, port=8080, debug=True)
httpserver.serve(app, host=DOMAIN, port=8080)
