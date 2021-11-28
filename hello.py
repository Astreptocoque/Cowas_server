from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request
from flask import render_template
from werkzeug.utils import redirect
from flask import session
from datetime import timedelta

app = Flask(__name__)

# warning session is stored on client browser. Server cannot logout user.
app.secret_key = "7,1Iaz{eaW3(Nux9?;>qPAm]O]s5vB"
app.permanent_session_lifetime = timedelta(minutes=10)

# ===== VARIABLES =======
led_state = None
button_state = None

@app.before_request
def before_request():
    print("initiate")


@app.route("/")
def root():
    return redirect(url_for("home"))

@app.route("/home/")
def home():
    return render_template("home.html")

# get LED state to update Arduino board
@app.route("/control/")
def get_led_state():
    global led_state
    led_state_p = request.args.get("query")
    if led_state_p == "led":
        return f'{escape(led_state)}'

# receive information from Arduino board
@app.route("/update", methods=["POST"])
def update():
    global button_state
    button_state = request.args.get("button_state")
    print(button_state)
    return f'{escape("button updated")}'

# monitor information from Arduino board
@app.route("/monitor/", methods=["GET","POST"])
def monitor():
    global button_state
    # print(button_state)
    if request.method == "POST":
        return render_template("monitor.html", message = button_state)
    else:
        return render_template("monitor.html", message = button_state)


# Login to control Arduino board
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
            return render_template("home.html", message = "Already logged.")
        else:
            return render_template("login.html")
	    

@app.route("/led/", methods=['GET','POST'])
def led_control():
    global led_state

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


@app.route('/logout')
def logout():

    session.pop('user', None)
    logged_IP_adress = None
    return redirect(url_for('login'))
