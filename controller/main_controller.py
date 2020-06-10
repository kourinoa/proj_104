from flask import Flask, request
from flask import render_template
import etl_serv

app = Flask(__name__, template_folder="../view/templates", static_folder="../view/static")
app.config["DEBUG"] = True


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    keyword = request.values.get("keyword")
    page_num = request.values.get("pagenum")
    etl_serv.do_search(keyword, page_num)
    return keyword + " , " + page_num


if __name__ == "__main__":
    app.run()