from flask import Flask, url_for
import click

app = Flask(__name__)

app.config['ADMIN_NAME'] = "admin"
app.config.update(
    TESTING=True,
    SECRET_KEY='_5#yF4Q8z\n\xec]/'
)
# print(app.config['ADMIN_NAME'])
# print(app.config['TESTING'])
# print(app.config['SECRET_KEY'])

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello Flask!</h1>'

@app.route('/greet', defaults={'name': ''})
@app.route('/greet/', defaults={'name': ''})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello %s!</h1>' % name


with app.test_request_context():
    print(url_for("greet", _external=True, name="zhangsan"))




# @app.cli.command("say-hello")
@app.cli.command()
def hello():
    """Just say hello."""
    click.echo('Hello, Human!')


print(app.url_map)
if __name__ == '__main__':
    app.run()
