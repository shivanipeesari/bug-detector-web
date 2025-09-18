from flask import Flask, render_template, request
from detector import analyze_code

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    issues = []
    code = ""
    if request.method == "POST":
        code = request.form["code"]
        issues = analyze_code(code)
    return render_template("index.html", issues=issues, code=code)

if __name__ == "__main__":
    app.run(debug=True)

