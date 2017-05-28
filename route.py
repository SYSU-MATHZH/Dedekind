import sqlite3
import bottle
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './tmp',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)


def login_check(session):
    user_id = session.get('user_id', -1)
    user_id_cookie = bottle.request.get_cookie('user_id', secret='rbtail')
    if user_id_cookie is None:
        session['user_id'] = -1
        return False
    else:
        if user_id == -1:
            session['user_id'] = user_id_cookie
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
        return "Project Dedekind!" + " code: " + str(code) + " name: " + str(name) + " email: " + str(email) + " suahours: " + str(suahours)
    else:
        bottle.redirect('/login')


@bottle.route('/login')
def login():
    s = bottle.request.environ.get('beaker.session')
    if login_check(s):
        bottle.redirect('/')
    else:
        return bottle.template('login')


@bottle.route('/login', method='POST')
def do_login():
    username = bottle.request.forms.get('user_name')
    password = bottle.request.forms.get('user_password')
    isSaveStatus = bottle.request.forms.get('loginstatus')
    print(isSaveStatus)
    conn = sqlite3.connect('db_dedekind.db')
    cur = conn.cursor()
    cur.execute('''SELECT user_id, user_password
                    FROM Users
                    WHERE user_code = :user_code''',
                {'user_code': username})
    result = cur.fetchone()
    if result is not None:
        user_id, user_password = result
        if password == str(user_password):
            s = bottle.request.environ.get('beaker.session')
            s['user_id'] = int(user_id)
            if isSaveStatus:
                print(isSaveStatus)
                bottle.response.set_cookie(
                    'user_id', int(user_id), secret='rbtail', max_Age=5*24*3600)
            else:
                bottle.response.set_cookie(
                    'user_id', int(user_id), secret='rbtail', max_Age=-1)

        else:
            conn.close()
            bottle.redirect('/login')
    else:
        conn.close()
        bottle.redirect('/login')
    conn.close()
    bottle.redirect('/')


@bottle.route('/logout')
def logout():
    s = bottle.request.environ.get('beaker.session')
    if login_check(s):
        s['user_id'] = -1
        bottle.response.delete_cookie('user_id', secret='rbtail')
    bottle.redirect('/')


bottle.run(app=app, host='0.0.0.0', port=8080, debug=True)
