from flask import Flask, render_template, request, jsonify, session
import traceback
import datetime
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'pyanalyzer-secret-key-2024'

# Analytics storage (in-memory for demo)
analytics = {
    'total_analyses': 0,
    'errors_found': 0,
    'fixed_errors': 0,
    'ai_chats': 0,
    'error_breakdown': defaultdict(int),
    'recent_activities': []
}


def track_activity(activity_type, title):
    """Track user activity"""
    analytics['recent_activities'].insert(0, {
        'type': activity_type,
        'title': title,
        'time': datetime.datetime.now().strftime("%H:%M")
    })
    # Keep only last 10 activities
    analytics['recent_activities'] = analytics['recent_activities'][:10]


def get_error_breakdown():
    """Convert defaultdict to regular dict for template"""
    return dict(analytics['error_breakdown'])

errors = {
    "SyntaxError": {
        "description": "This happens when Python finds invalid syntax in your code.",
        "solution": "Check missing quotes, brackets, colons, or incorrect indentation.",
        "example": 'print("Hello"',
        "fixed_code": 'print("Hello")',
        "notes": "A SyntaxError stops the program before it starts."
    },
    "NameError": {
        "description": "This happens when you use a variable or function name that has not been defined.",
        "solution": "Make sure the variable or function exists before using it.",
        "example": 'print(x)',
        "fixed_code": 'x = 10\nprint(x)',
        "notes": "Check spelling carefully."
    },
    "TypeError": {
        "description": "This happens when an operation is used with the wrong data type.",
        "solution": "Make sure the data types are compatible.",
        "example": 'print("Age: " + 20)',
        "fixed_code": 'print("Age: " + str(20))',
        "notes": "You often need conversion like str(), int(), or float()."
    },
    "ValueError": {
        "description": "This happens when a function gets the correct type but an invalid value.",
        "solution": "Use a valid value for the function.",
        "example": 'int("abc")',
        "fixed_code": 'number = int("123")',
        "notes": "The type may be correct, but the value itself is not acceptable."
    },
    "IndexError": {
        "description": "This happens when you try to access a list index that does not exist.",
        "solution": "Make sure the index is within the valid range.",
        "example": 'my_list = [1, 2, 3]\nprint(my_list[5])',
        "fixed_code": 'my_list = [1, 2, 3]\nprint(my_list[2])',
        "notes": "Python list indexing starts at 0."
    },
    "KeyError": {
        "description": "This happens when you try to access a dictionary key that does not exist.",
        "solution": "Use an existing key or check before accessing it.",
        "example": 'data = {"name": "Salem"}\nprint(data["age"])',
        "fixed_code": 'data = {"name": "Salem"}\nprint(data.get("age", "Key not found"))',
        "notes": "Using dict.get() is safer."
    },
    "ZeroDivisionError": {
        "description": "This happens when you divide a number by zero.",
        "solution": "Make sure the divisor is not zero.",
        "example": 'print(10 / 0)',
        "fixed_code": 'divisor = 2\nprint(10 / divisor)',
        "notes": "Division by zero is mathematically undefined."
    },
    "IndentationError": {
        "description": "This happens when indentation is incorrect in Python code.",
        "solution": "Make sure blocks are indented properly.",
        "example": 'if True:\nprint("Hello")',
        "fixed_code": 'if True:\n    print("Hello")',
        "notes": "Python uses indentation to define code blocks."
    },
    "AttributeError": {
        "description": "This happens when an object does not have the attribute or method you called.",
        "solution": "Check the object type and available methods.",
        "example": 'x = 10\nx.append(5)',
        "fixed_code": 'numbers = [10]\nnumbers.append(5)',
        "notes": "append() works on lists, not integers."
    },
    "ModuleNotFoundError": {
        "description": "This happens when Python cannot find the module you are trying to import.",
        "solution": "Install the module or check its name.",
        "example": 'import numppy',
        "fixed_code": 'import numpy',
        "notes": "Make sure the spelling is correct and the package is installed."
    }
}


def default_result(error_name="No Error", description="No issue found.", solution="Your code looks fine.",
                   example="", fixed_code="No fix needed. Your code is already correct.",
                   notes="No additional notes."):
    return {
        "description": description,
        "solution": solution,
        "example": example,
        "fixed_code": fixed_code,
        "notes": notes
    }


def analyse_code(code):
    code = code.strip()

    if not code:
        return "Empty Input", default_result(
            error_name="Empty Input",
            description="No code was entered.",
            solution="Please paste or write Python code first.",
            example="",
            fixed_code="",
            notes="The analyser needs some code to check."
        )

    if ".append(" in code and "=" in code:
        lines = code.splitlines()
        for line in lines:
            clean = line.strip()
            if clean.startswith(("x =", "y =", "z =", "num =", "value =")) and ".append(" not in clean:
                if "[]" not in clean and "[" not in clean:
                    return "AttributeError", default_result(
                        error_name="AttributeError",
                        description="You may be using append() on a non-list object.",
                        solution="append() only works with lists.",
                        example='x = 10\nx.append(5)',
                        fixed_code='x = [10]\nx.append(5)',
                        notes="Check the variable type before calling append()."
                    )

    try:
        compiled_code = compile(code, "<string>", "exec")
    except SyntaxError as e:
        line_text = ""
        if e.text:
            line_text = e.text.strip()

        error_data = default_result(
            error_name="SyntaxError",
            description=f"Python found invalid syntax on line {e.lineno}.",
            solution="Check brackets, quotes, colons, and indentation.",
            example=line_text,
            fixed_code="Please review the line shown above and correct the syntax.",
            notes=f"Details: {e.msg}"
        )
        return "SyntaxError", error_data

    try:
        exec_globals = {}
        exec(compiled_code, exec_globals)
        return "No Error", default_result()

    except Exception as e:
        error_type = type(e).__name__
        tb = traceback.format_exc()

        if error_type in errors:
            error_data = errors[error_type].copy()
            error_data["notes"] += f"\n\nDetected details: {str(e)}"
            error_data["example"] = code
            return error_type, error_data

        return error_type, default_result(
            error_name=error_type,
            description=f"A runtime error occurred: {error_type}",
            solution="Check the code logic and the error details.",
            example=code,
            fixed_code="Review your variables, function calls, and data types.",
            notes=tb
        )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    import datetime
    return render_template("dashboard.html",
        last_update=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        total_analyses=analytics['total_analyses'],
        errors_found=analytics['errors_found'],
        fixed_errors=analytics['fixed_errors'],
        ai_chats=analytics['ai_chats'],
        error_breakdown=get_error_breakdown(),
        max_count=max(analytics['error_breakdown'].values()) if analytics['error_breakdown'] else 0,
        errors_list=list(errors.keys()),
        recent_activities=analytics['recent_activities']
    )


@app.route("/about")
def about():
    return render_template("about.html", errors=list(errors.keys()))


@app.route("/error-search")
def error_search():
    return render_template("error_search.html", errors_list=list(errors.keys()))


@app.route("/code-analyzer")
def code_analyzer():
    return render_template("code_analyzer.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    user_code = request.form.get("code", "")
    error_name, data = analyse_code(user_code)

    # Track analytics
    analytics['total_analyses'] += 1
    if error_name != "No Error" and error_name != "Empty Input":
        analytics['errors_found'] += 1
        analytics['error_breakdown'][error_name] += 1
        track_activity('error', f'Found {error_name}')
    else:
        analytics['fixed_errors'] += 1
        track_activity('analyze', 'Code analyzed - No errors')

    return render_template(
        "result.html",
        error=error_name,
        data=data,
        user_code=user_code
    )


@app.route("/result", methods=["POST"])
def result():
    user_error = request.form.get("error", "").strip()

    if user_error in errors:
        data = errors[user_error]
    else:
        data = {
            "description": "Error not found.",
            "solution": "Try another error name exactly as written.",
            "example": "",
            "fixed_code": "",
            "notes": "No suggested fix available."
        }

    return render_template("result.html", error=user_error, data=data, user_code="")


@app.route("/quick-error/<error_name>")
def quick_error(error_name):
    if error_name in errors:
        data = errors[error_name]
    else:
        data = {
            "description": "Error not found.",
            "solution": "Try another error name exactly as written.",
            "example": "",
            "fixed_code": "",
            "notes": "No suggested fix available."
        }

    return render_template("result.html", error=error_name, data=data, user_code="")


@app.route("/api/ai-chat", methods=["POST"])
def ai_chat():
    query = request.get_json().get('message', '').lower()

    # Track AI chat
    analytics['ai_chats'] += 1

    responses = {
        "syntax": "SyntaxError: Code has invalid syntax. Check brackets, quotes, colons!",
        "name": "NameError: You're using a variable that doesn't exist. Define it first!",
        "type": "TypeError: Wrong data type. Use str(), int(), float() to convert!",
        "index": "IndexError: List index out of range. Remember Python starts at 0!",
        "key": "KeyError: Dictionary key doesn't exist. Use .get() method!",
        "help": "I can help with: SyntaxError, NameError, TypeError, IndexError, KeyError, and more!"
    }
    for k, v in responses.items():
        if k in query:
            track_activity('chat', f'Asked about {k}')
            return jsonify({'response': v})
    track_activity('chat', f'Asked: {query[:20]}...')
    return jsonify({'response': f"I understand you're asking about '{query}'. Ask me about any Python error!"})


if __name__ == "__main__":
    app.run(debug=True)
