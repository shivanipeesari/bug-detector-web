import ast

def analyze_code(code):
    issues = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and len(node.body) == 0:
                issues.append({"type": "Empty function", "line": node.lineno, "name": node.name})
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
                issues.append({"type": "Unsafe eval usage", "line": node.lineno})
    except Exception as e:
        issues.append({"type": "Parse error", "error": str(e)})
    return issues

