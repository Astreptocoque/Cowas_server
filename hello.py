from os import truncate
from flask import Flask, sessions
from markupsafe import escape #protection contre des attaques
from flask import url_for
from flask import request
from flask import Response
from flask import render_template
from werkzeug.utils import redirect
from flask import session
from datetime import timedelta

# https://flask.palletsprojects.com/en/2.0.x/quickstart/

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.before_request
def before_request():
    print("initiate")
    # g.led_state = 1 #global variable

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/led_state/<int:led_state>")
def led_toggle(led_state):
    return f'Led {escape(led_state)}'

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        session.permanent = True
        session["user"] = username

        # If correct, go to LED control page, otherwise redo
        if username == "Tim" and password == "cowas":
            return redirect(url_for("led_control"))
        else:
            return render_template("login.html", message = "Wrong credentials")
    # GET request
    else:
        if "username" in session:
            return redirect(url_for("led_control"))
        else:
            pass    
	    return render_template("login.html")

@app.route("/led/", methods=['GET','POST'])
def led_control():

    if "user" in session:

        if request.method == "POST":
            if request.form.get("Led_toggle") == 'pressed':
                # if(g.led_state == 0):
                #     message = "LED is ON"
                #     g.led_state = 1
                #     print("LED 1")
                # else:
                #     message = "LED is OFF"
                #     g.led_state = 0
                #     print("LED 0")
                #     print(g.led_state)
                pass
        # GET request
        elif request.method == "GET":
            return render_template("Led_control.html")
        return render_template("Led_control.html", message="message")
    
    else:
        redirect(url_for("login"))

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))