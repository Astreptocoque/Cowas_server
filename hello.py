from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request
from flask import render_template
from werkzeug.utils import redirect
from flask import session
from datetime import timedelta, datetime
from flask import jsonify
import copy

app = Flask(__name__)

# THIS IS NOT SECURED AT ALL
app.secret_key = "7,1Iaz{eaW3(Nux9?;>qPAm]O]s5vB"
app.permanent_session_lifetime = timedelta(minutes=10)

# ===== VARIABLES =======
led_state = None
button_state = None

class Sample:
    def __init__(self, _datem, _frequency, _depth):
        self.datem = _datem
        self.frequency = _frequency
        self.depth = _depth

sample = Sample(datetime(1970, 1, 1), 0, 0)

@app.before_request
def before_request():
    print("initiate")


@app.route("/")
def root():
    return redirect(url_for("home"))

@app.route("/home/")
def home():
    return render_template("home.html")

@app.route("/samples/")
def get_sample():
    global sample
    sample_p = request.args.get("querry")
    #if sample_p == "led"
    sample2 = copy.deepcopy(sample)
    sample = Sample(datetime(1970, 1, 1), 0, 0)
    return jsonify(year=sample2.datem.year,
        month= sample2.datem.month,
        day= sample2.datem.day,
        hour= sample2.datem.hour,
        minute= sample2.datem.minute,
        frequency= sample2.frequency,
        depth= sample2.depth)

# set samples
@app.route("/samples/create", methods=['GET', 'POST'])
def set_sample():
    global sample
    if request.method == "POST":
        datem = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        print(datem)
        frequency = int(request.form.get('frequency'))
        depth = int(request.form.get('depth'))

        if depth <= 0 and depth > 40000:
            return render_template("New_sample.html", message = "Depth invalid")
        else:
            sample.datem = datem
            sample.frequency = frequency
            sample.depth = depth
            return render_template("New_sample.html", message = "ENJOY !")
    # GET request
    else:
        if "user" in session:
            return render_template("New_sample.html")
        else:
            return render_template("login.html")

# receive information from Arduino board
@app.route("/update", methods=["POST"])
def update():
    global button_state
    # button_state = request.args.get("button_state")
    content = request.get_json()
    print(content)
    button_state = content["value"]

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


@app.route('/logout')
def logout():

    if "user" in session:
        session.pop('user', None)
        logged_IP_adress = None
        return redirect(url_for('login'))
    else:
        return redirect(url_for("login"))
