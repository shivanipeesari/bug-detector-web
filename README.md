# 🐞 Bug Detector Web

A simple web application built with Python and Flask that uses the Gemini API to detect bugs in your Python code.

## ✨ Features

* **Interactive Web Interface**: Paste your Python code into a user-friendly web form.
* **AI-Powered Bug Detection**: Leverages the power of the Gemini API to analyze code for potential errors and issues.
* **Secure API Key Management**: Uses a `.env` file to keep your private API key safe and out of the public repository.

## 🚀 Getting Started

Follow these steps to get a copy of the project up and running on your local machine.

### **Prerequisites**

* **Python 3.x**
* **Git**

### **Installation**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/shivanipeesari/bug-detector-web.git](https://github.com/shivanipeesari/bug-detector-web.git)
    cd bug-detector-web
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    * **macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```
    * **Windows**:
        ```bash
        venv\Scripts\activate
        ```

4.  **Install the required libraries:**
    The project uses a `requirements.txt` file to manage dependencies.
    ```bash
    pip install -r requirements.txt
    ```
    *If you get an error that `requirements.txt` doesn't exist, install the dependencies manually:*
    ```bash
    pip install flask google-generativeai python-dotenv
    ```

### **API Key Configuration**

This project requires a **Gemini API Key**. For security, the key should not be committed to Git.

1.  Get your free API key from [Google AI Studio](https://ai.google.dev/).
2.  In the root directory of your project, create a file named **`.env`**.
3.  Add your API key to this file in the following format:
    ```
    GEMINI_API_KEY='YOUR_ACTUAL_API_KEY'
    ```

> **Note:** The `.gitignore` file is configured to prevent the `.env` file from being uploaded to Git.

### **Running the Application**

With the virtual environment active and your `.env` file configured, you can now run the Flask application.

```bash
python app.py
