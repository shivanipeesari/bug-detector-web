import google.generativeai as genai
import os
import re
import json
from typing import List, Dict, Any

# Configure the Gemini API with your API key
# Ensure you have set the environment variable GEMINI_API_KEY with your key.
# For example, on Linux/macOS: export GEMINI_API_KEY="YOUR_API_KEY"
# On Windows: set GEMINI_API_KEY="YOUR_API_KEY"
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
except ValueError as e:
    print(f"Configuration Error: {e}")
    exit()

def detect_bugs(code: str) -> List[Dict[str, Any]]:
    """
    Uses the Gemini API to analyze Python code and detect bugs.
    Returns a list of issues with type, description, line number, function name, and code line.
    """
    issues = []
    lines = code.split('\n')

    # Prompt for Gemini to analyze the code
    prompt = f"""
    Analyze the following Python code for bugs and return a JSON object with the following structure for each issue:
    - "type": string (e.g., "SyntaxError", "NameError", "Missing Colon", etc.),
    - "description": string (detailed explanation of the bug),
    - "line": integer (line number where the bug occurs),
    - "name": string or null (function name if applicable, else null),
    - "code_line": string (the exact line of code with the bug).

    Code:
    ```
    {code}
    ```

    Provide the response as a JSON array, even if no issues are found (return empty array [] if no bugs).
    """

    try:
        # Generate content using Gemini (e.g., gemini-1.5-pro model)
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        
        # Extract JSON from response.
        json_str = response.text.strip()
        
        # Clean up the response to ensure it's valid JSON
        # Some models may return a markdown code block, so we'll remove it.
        if json_str.startswith('```json'):
            json_str = json_str.replace('```json', '').replace('```', '').strip()
            
        issues_data = json.loads(json_str) if json_str else []

        # Validate and structure the issues
        for issue in issues_data:
            if not all(key in issue for key in ['type', 'description', 'line', 'name', 'code_line']):
                continue  # Skip malformed entries
            
            # Use line number to fetch the actual code line
            # Ensure line number is valid and within the bounds of the code
            line_num = int(issue['line']) - 1
            code_line = lines[line_num].strip() if 0 <= line_num < len(lines) else issue['code_line']
            
            issues.append({
                'type': issue['type'],
                'description': issue['description'],
                'line': int(issue['line']),
                'name': issue['name'] if issue['name'] else None,
                'code_line': code_line
            })

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from Gemini API response: {e}")
        print(f"Raw response text: \n{response.text}")
        issues = [{
            'type': 'API Response Error',
            'description': f"Failed to parse JSON from API. Raw response: {response.text}",
            'line': 1,
            'name': None,
            'code_line': lines[0] if lines else ''
        }]
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        # Fallback: Return a generic issue if the API call fails
        issues = [{
            'type': 'API Error',
            'description': f"Failed to analyze code: {str(e)}",
            'line': 1,
            'name': None,
            'code_line': lines[0] if lines else ''
        }]

    return issues

# Example Usage
if __name__ == "__main__":
    # Sample buggy code to be analyzed
    buggy_code = """
def calculate_area(radius):
    # Missing colon here
    if radius > 0
        return 3.14 * radius * radius

def divide(a, b):
    # Potential ZeroDivisionError if b is 0
    result = a / b
    print("Result is:", result)

def main():
    x = 10
    y = "5" # Type mismatch
    z = x + y

    area = calculate_area(-5)
    
    divide(10, 0) # This will cause a runtime error
    
    # Missing variable 'my_var'
    print(my_var)
"""

    print("Analyzing the following code for bugs:")
    print("--------------------------------------")
    print(buggy_code)
    print("--------------------------------------")
    
    detected_bugs = detect_bugs(buggy_code)
    
    if detected_bugs:
        print("\nBugs detected:")
        for bug in detected_bugs:
            print(f"\nType: {bug['type']}")
            print(f"Description: {bug['description']}")
            print(f"Function Name: {bug['name'] or 'N/A'}")
            print(f"Line: {bug['line']}")
            print(f"Code Line: {bug['code_line']}")
    else:
        print("\nNo bugs detected.")
