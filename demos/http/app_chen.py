# -*- coding: utf-8 -*-

from flask import Flask, request, url_for, redirect, abort, make_response, jsonify, session, escape, g
import json
import os
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum


app = Flask(__name__)

# @app.route('/hello', methods=["GET","POST"])
# def hello():
#     name = request.args.get('name', None)    # 获取查询参数name的值
#     if name is None:
#         name = request.cookies.get("name", None) # 从Cookie中取值
#         if name is None:
#             return abort(500)
#     return '<h1>Hello, %s!</h1>' % name     # 插入到返回值中

@app.route('/go_back/<int:year>')
def go_back(year):
    return "Welcome to %d" % (2018 - year)

@app.route('/colors/<any(blue,white,red):color>')
def three_colors(color):
    return "<p>Color is %s.</p>" % color


@app.route('/hello2')
def hello2():
    return '<h1>Hello2, Flask!</h1>'

@app.route('/hello3')
def hello3():
    return '<h1>Hello3, Flask!</h1>', 201

@app.route('/hello4')
def hello4():
    return '', 302, {'Location':"http://example.com", 'aaa':"111"} #重定向到指定网址


@app.route('/hi')
def hi():
    return redirect(url_for('hello'), 301)


# return error response
@app.route('/brew/<drink>')
def teapot(drink):
    if drink == 'coffee':
        abort(418)
    else:
        return 'A drop of tea.'

@app.route('/404')
def not_found():
    abort(404)


@app.route('/foo1')
def foo1():
    response = make_response("""<!DOCTYPE html>
        <html>
        <head></head>
        <body>
            <h1>Note</h1>
            <p>to: Peter</p>
            <p>from: Jane</p>
            <p>heading: Reminder</p>
            <p>body: <strong>Don't forget the party!</strong></p>
        </body>
        </html>
    """) #使用make_response()生成响应对象
    response.mimetype = 'text/html' #修改响应头中的MIME类型
    return response

@app.route('/foo2')
def foo2():
    response = make_response("""<?xml version="1.0" encoding="UTF-8"?>
        <note>
            <to>Peter</to>
            <from>Jane</from>
            <heading>Reminder</heading>
            <body>Don't forget the party!</body>
        </note>
     """)
    response.headers['Content-Type'] = 'text/xml; charset=utf-8' #设置响应头中Content-Type值
    return response

@app.route('/foo3')
def foo3():
    return "hello, World3!", {"Content-Type": "text/plain; charset=utf-8"} #设置响应头中Content-Type值

@app.route('/foo4')
def foo4():
    body = {
    "note":{
        "to":"Peter",
        "from":"Jane",
        "heading":"Reminder",
        "body":"Don't forget the party!"
    }
}
    #这种方法不需要指定MIME类型
    response = jsonify(body) #JSON格式序列化为Response JSON->Response, jsonify还支持接收dict参数、关键字
    # equal to:
    #这种方法需要指定MIME类型
    # response = make_response(json.dumps(body)) #JSON格式序列化为String
    # response.mimetype = "application/json"
    return response


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for("hello")))
    response.set_cookie("name", name)
    return response


app.secret_key = os.getenv("SECRET_KEY", "")

@app.route('/login')
def login():
    session['logged_in'] = True # 向session中添加了一个名为"logged_in"的cookie
    session['username'] = "Admin"
    session.permanent = True #默认31天
    app.permanent_session_lifetime  = 3600 * 24
    # 等效于 配置环境变量 PERMANENT_SESSION_LIFETIME
    return redirect(url_for('hello'))

@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
    response = '<h1>Hello, %s!</h1>' % escape(name)  # escape name to avoid XSS
    # return different response according to the user's authentication status
    #验证是否存在
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    #验证session的指定key的值
    if session.get("username") == name:
        response += '<h1>管理员</h1>'
    else:
        response += "<h1>用户</h1>"

    return response


@app.route('/admin')
def admin():
    print (g.name)
    if "logged_in" not in session:
        abort(403)
    return "Welcome to admin page."


@app.route("/logout")
def logout():
    if "logged_in" in session:
        session.pop("logged_in")
    return redirect(url_for("hello"))


@app.route('/foo')
def foo():
    print(is_safe_url("http://www.baidu.com/aaa/111"))
    print(is_safe_url("http://127.0.0.1/bbb"))
    return '<h1>Foo page</h1><a href="%s">Do something</a>' % url_for('do_something')

@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something </a>' % url_for('do_something', next=request.full_path)

@app.route('/do-something')
def do_something():
    # do something
    # return redirect(request.referrer) #请求头里的referer参数，自动记录上一个页面URL
    # return redirect(request.referrer or url_for("hello")) #获取请求头里的referer参数 + 缺省值
    # return redirect(request.args.get("next", url_for("hello"))) #获取URL里的next参数 + 缺省值
    return redirect_back()


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    print("request.host_url", request.host_url)
    print("ref_url", ref_url)
    test_url = urlparse(urljoin(request.host_url, target))
    print("urljoin(request.host_url, target)", urljoin(request.host_url, target))
    print("test_url", test_url)
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


# AJAX
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data){
                $('.body').append(data);
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)

#钩子
@app.before_request
def do_something():
    # 这里的代码会在每个请求处理前执行
    print ("我做了某事，在请求前！")


#当前请求中的全局变量，每次请求都会重设
@app.before_request
def get_name():
    g.name = request.args.get('name')


# from flask import current_app

# #手动激活程序上下文
# with app.app_context():
#     print(current_app.name)
#
# #手动激活程序上下文 push方法
# app_ctx = app.app_context()
# app_ctx.push() #推送
# print(current_app.name)
# app_ctx.pop() #销毁
#
# #手动激活请求上下文
# with app.test_request_context('/hello'):
#     print(request.method)
#
# #手动激活请求上下文 push方法
# app_req_ctx = app.test_request_context('/hello')
# app_req_ctx.push()
# print(request.method)
# app_req_ctx.pop()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)