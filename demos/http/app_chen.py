# -*- coding: utf-8 -*-

from flask import Flask, request, url_for
import click

app = Flask(__name__)

@app.route('/hello')
def hello():
    name = request.args.get('name', 'Flask')    # 获取查询参数name的值
    return '<h1>Hello, %s!</h1>' % name     # 插入到返回值中

#路由表
@app.cli.command("route")
def cli_route():
    """显示应用中所有的路由 来自app.url_map"""
    click.echo(app.url_map)

if __name__ == "__main__":
    app.run()