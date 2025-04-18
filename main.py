from flask import Flask, render_template, request, session
from livereload import Server
from dotenv import load_dotenv
import ast
import os
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def home():
    try:
        print("⭐", session["result"])
    except Exception:
        print("❌No session result")
    if "result" not in session:
        session['result'] = ""

    if request.method == "POST":
        value = request.form.get("button")
        print(type(value))
        # session["value_type"] = type(value)

        if value == "C":
            session["result"] = ""
        elif value == "=":
            try:

                session["result"] = str(eval(session["result"]))
                print(f"eval done {session['result']}")
            except Exception:
                print("❌ Houston we have problem ❌")
                session["result"] = "ERROR"
        elif value == "<":
            session['result'] = session['result'][:-1]


        else:
            print(f"{session['result']} appending {value}")
            session["result"] += str(value)

    return render_template("index.html", result=session["result"])


if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch("templates/")
    server.watch("static/")
    server.serve(debug=True, host="0.0.0.0", port=5000)
