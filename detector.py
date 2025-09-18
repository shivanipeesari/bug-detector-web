import ast

def analyze_code(code):
    issues = []
    
    # Check for basic syntax errors first
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        issues.append({
            "type": "SyntaxError",
            "line": e.lineno,
            "error": str(e),
            "code_line": code.splitlines()[e.lineno - 1].strip()
        })
        return issues
    except Exception as e:
        issues.append({
            "type": "Parse Error",
            "line": "N/A",
            "error": f"An unexpected error occurred during parsing: {str(e)}"
        })
        return issues

    # Walk through the code's abstract syntax tree to find issues
    for node in ast.walk(tree):
        
        # Bug Type 1: Empty Function/Class/Loop
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.If, ast.For, ast.While, ast.With)) and not node.body:
            issues.append({
                "type": "Empty Block",
                "line": node.lineno,
                "error": f"An empty {type(node).__name__} block was found.",
                "code_line": code.splitlines()[node.lineno - 1].strip()
            })
            
        # Bug Type 2: Unsafe 'eval' or 'exec' usage
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ("eval", "exec"):
                issues.append({
                    "type": "Security Warning (Unsafe Function)",
                    "line": node.lineno,
                    "error": f"The use of '{node.func.id}' can be a security risk. Avoid using it with untrusted input.",
                    "code_line": code.splitlines()[node.lineno - 1].strip()
                })
        
        # Bug Type 3: Missing 'return' statement in a function
        if isinstance(node, ast.FunctionDef):
            has_return = any(isinstance(body_node, ast.Return) for body_node in ast.walk(node))
            if not has_return:
                issues.append({
                    "type": "Missing Return",
                    "line": node.lineno,
                    "error": f"Function '{node.name}' does not have a return statement. It will implicitly return None.",
                    "code_line": f"def {node.name}(...):"
                })
                
        # Bug Type 4: Unassigned variables used in a loop (logic bug)
        # This is a more complex check and would require a deeper analysis of variable scope
        # For a simple example, we can check for variables that are not defined before use.
        # This is not a perfect solution but gives a better example.
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            is_defined = False # Placeholder for a proper check
            # Real implementation would need to track variable assignments
            # For demonstration, let's assume 'undefined_var' is a bug.
            if node.id == "undefined_var":
                issues.append({
                    "type": "Undefined Variable",
                    "line": node.lineno,
                    "error": f"Variable '{node.id}' might be used before it is assigned.",
                    "code_line": code.splitlines()[node.lineno - 1].strip()
                })
                
    return issues

