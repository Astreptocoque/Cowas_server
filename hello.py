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

app = Flask(__name__)

app.secret_key = Flask.secret_key
app.permanent_session_lifetime = timedelta(minutes=10)

led_state = None

@app.before_request
def before_request():
    global led_state
    # led_state = 0
    print("initiate")

@app.route("/")
def root():
    return redirect(url_for("home"))

@app.route("/home/")
def home():
    return render_template("home.html")

@app.route("/control/")
def get_led_state():
    global led_state
    led_state_p = request.args.get("querry")
    if led_state_p == "led":
        return f'{escape(led_state)}'

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
    
        # If correct, go to LED control page, otherwise redo
        if username == "Tim" and password == "cowas":
            session.permanent = True
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", message = "Wrong credentials")
    # GET request
    else:
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("login.html")    
	    

@app.route("/led/", methods=['GET','POST'])
def led_control():
    global led_state
    if "user" in session:

        if request.method == "POST":
            if request.form.get("On") == 'On':
                print("ON selected")
                led_state = 1
                print(led_state)
                message = "On selected"
            elif request.form.get("Off") == 'Off':
                print("Off selected")
                led_state = 0
                print(led_state)
                message = "OFF selected"
            else:
                pass

        # GET request
        elif request.method == "GET":
            message = "Choose an action"
        return render_template("Led_control.html", message=message)
    else:
        return redirect(url_for("login"))

# ###############################################
# #          Render monitoring page              #
# ###############################################
# @app.route('/monitoring', methods=["GET", "POST"])
# def monitoring():
#     if "user" in session:
#         return render_template("Monitoring.html")
#     else:
#         redirect(url_for("login"))

# ###############################################
# #          Render control page              #
# ###############################################
# @app.route('/control', methods=["GET", "POST"])
# def control():
#     if "user" in session:
#         return render_template("Control.html")
#     else:
#         redirect(url_for("login"))


# @app.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr}</h1>"

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user', None)
    return redirect(url_for('login'))