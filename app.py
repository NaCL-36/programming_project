
from flask import Flask

from flask import Flask, render_template, request
from errors_data import errors


app = Flask(__name__)

@app.route("/")
def home():


    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    user_error = request.form.get("error")

    if user_error in errors:
        data = errors[user_error]
    else:
        data = {
            "description": "Error not found.",
            "solution": "Try another error.",
            "example": ""
        }

    return render_template("result.html", error=user_error, data=data)


if __name__ == "__main__":
    app.run(debug=True)