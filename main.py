from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/create/acc")
def create_acc_page():
    return render_template("create_acc.html")

if __name__ == "__main__":

    app.run("0.0.0.0", port=8080, debug=True)
