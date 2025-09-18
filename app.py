
from flask import Flask, render_template, request
from detector import detect_bugs

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    code = ""
    issues = []
    
    if request.method == 'POST':
        code = request.form.get('code', '')
        issues = detect_bugs(code)
    
    return render_template('index.html', code=code, issues=issues)

if __name__ == '__main__':
    app.run(debug=True)
