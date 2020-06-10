import flask
from flask import render_template

app = flask.Flask(__name__, template_folder="../view/templates", static_folder="../view/static")
app.config["DEBUG"] = True


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    return ""


if __name__ == "__main__":
    app.run()