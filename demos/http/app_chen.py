# -*- coding: utf-8 -*-

from flask import Flask, request, url_for, redirect, abort, make_response, jsonify
import json


app = Flask(__name__)

@app.route('/hello', methods=["GET","POST"])
def hello():
    name = request.args.get('name', None)    # 获取查询参数name的值
    if name is None:
        name = request.cookies.get("name", None) # 从Cookie中取值
        if name is None:
            return abort(500)
    return '<h1>Hello, %s!</h1>' % name     # 插入到返回值中

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


@app.route('/foo')
def foo():
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

#钩子
@app.before_request
def do_something():
    # 这里的代码会在每个请求处理前执行
    print ("我做了某事，在请求前！")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)