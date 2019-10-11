from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Welcome to My Watchlist!"


def a():
    a = 10
    b = 20
    c = a - b
    pass

if __name__ == "__main__":
    app.run()


def b():
    pass