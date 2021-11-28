from flask import Flask
from markupsafe import escape #protection contre des attaques
from flask import url_for
from flask import request
from flask import render_template
from werkzeug.utils import redirect
from flask import session
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "7,1Iaz{eaW3(Nux9?;>qPAm]O]s5vB"
app.permanent_session_lifetime = timedelta(minutes=10)

# ===== VARIABLES =======
led_state = None
logged_IP_adress = None


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
    global logged_IP_adress

    remote_IP = request.remote_addr
    print("remote IP")
    print(remote_IP)
    print("stored IP")
    print(logged_IP_adress)

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
    
        # If correct, go to LED control page, otherwise redo
        if username == "Tim" and password == "cowas":
            session.permanent = True
            session["user"] = username
            logged_IP_adress = remote_IP
            return redirect(url_for("home"))
        else:
            return render_template("login.html", message = "Wrong credentials")
    # GET request
    else:
        # if nobody is connected
        if logged_IP_adress == None:
            return render_template("login.html")
        # if already connected
        elif logged_IP_adress == remote_IP:
            return redirect(url_for("home"))
        # if someone else already connected
        else:
            return render_template("home.html", message = "Someone is already connected. Please wait.")
	    

@app.route("/led/", methods=['GET','POST'])
def led_control():
    global led_state, logged_IP_adress

    # one user at a time
    if logged_IP_adress == request.remote_addr:

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
        return render_template("home.html", message = "Someone is already connected. Please wait.")

@app.route('/logout')
def logout():
    global logged_IP_adress

    # one user a time
    if logged_IP_adress == request.remote_addr:

        session.pop('user', None)
        logged_IP_adress = None
        return redirect(url_for('login'))

    else:
        return render_template("home.html", message = "Someone is already connected. Please wait.")
