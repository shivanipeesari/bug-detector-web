import os
from dotenv import load_dotenv
import google.generativeai as genai

# --- CHANGES START HERE ---
# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is set before configuring the API
if api_key:
    genai.configure(api_key=api_key)
else:
    # Handle the error if the key is not found
    print("Error: GEMINI_API_KEY not found. Please set it in your .env file.")
    # You might want to exit the application or handle this more gracefully
    # For now, we will continue, but the detector might fail.

# --- CHANGES END HERE ---

from flask import Flask, render_template, request
from detector import detect_bugs

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    code = ""
    issues = []
    
    if request.method == 'POST':
        code = request.form.get('code', '')
        # Only try to detect bugs if the API key is available
        if 'genai' in globals() and genai.configure:
            issues = detect_bugs(code)
        else:
            issues.append({"issue": "API key not set. Please check your .env file."})
    
    return render_template('index.html', code=code, issues=issues)

if __name__ == '__main__':
    app.run(debug=True)
