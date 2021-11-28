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

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.before_request
def before_request():
    session.permanent = True
    print("initiate")

@app.route("/")
def root():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/led_state/<int:led_state>")
def led_toggle(led_state):
    return f'Led {escape(led_state)}'

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
    
        # If correct, go to LED control page, otherwise redo
        if username == "Tim" and password == "cowas":
            session["User"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", message = "Wrong credentials")
    # GET request
    else:
        if "User" in session:
            return redirect(url_for("home"))
        else:
            return render_template("login.html")    
	    

@app.route("/led/", methods=['GET','POST'])
def led_control():

    if "user" in session:

        if request.method == "POST":
            if request.form.get("On") == 'On':
                print("ON selected")
                message = "On selected"
            elif request.form.get("Off") == 'Off':
                print("Off selected")
                message = "OFF selected"
            else:
                pass

        # GET request
        elif request.method == "GET":
            message = "Choose an action"
        return render_template("Led_control.html", message=message)


    else:
        redirect(url_for("login"))

###############################################
#          Render programme page              #
###############################################
@app.route('/monitoring', methods=["GET", "POST"])
def monitoring():
    if "user" in session:
        return render_template("Monitoring.html")
    else:
        redirect(url_for("login"))

###############################################
#          Render control page              #
###############################################
@app.route('/control', methods=["GET", "POST"])
def control():
    if "user" in session:
        return render_template("Control.html")
    else:
        redirect(url_for("login"))


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user', None)
    return redirect(url_for('home'))