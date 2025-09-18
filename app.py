from flask import Flask, render_template, request
import ast # Abstract Syntax Trees for parsing Python code

app = Flask(__name__)

# This function will analyze the code for simple bugs
def analyze_python_code(code):
    issues = []
    try:
        tree = ast.parse(code)
        
        # Example of a simple syntax check
        # This will catch basic syntax errors
        
        # Example of a simple bug check (e.g., unused variables)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # This is a placeholder for a more advanced check
                # For example, you could check for unused arguments
                pass

    except SyntaxError as e:
        # If there's a SyntaxError, capture it
        issues.append({
            'type': 'SyntaxError',
            'line': e.lineno,
            'code_line': code.splitlines()[e.lineno - 1].strip()
        })
    except Exception as e:
        # Catch other potential errors
        issues.append({
            'type': 'Unknown Error',
            'line': 'N/A',
            'code_line': str(e)
        })
        
    return issues

@app.route('/', methods=['GET', 'POST'])
def index():
    issues = None
    code = None
    if request.method == 'POST':
        code = request.form['code']
        issues = analyze_python_code(code)
        
    return render_template('index.html', code=code, issues=issues)

if __name__ == '__main__':
    app.run(debug=True)
