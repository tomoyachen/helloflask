from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Welcome to My Watchlist!"


def a():
    a = 1
    b = 2
    c = 1+2
    pass

if __name__ == "__main__":
    app.run()