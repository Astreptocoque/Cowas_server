from os import truncate
from flask import Flask
from markupsafe import escape #protection contre des attaques
from flask import url_for
from flask import request
from flask import Response
from flask import render_template
from werkzeug.utils import redirect
from flask import g
# https://flask.palletsprojects.com/en/2.0.x/quickstart/

app = Flask(__name__)
@app.before_request
def before_request():
    print("initiate")
    g.led_state = 1 #global variable

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/led_state/<int:led_state>")
def led_toggle(led_state):
    return f'Led {escape(led_state)}'

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')  # access the data inside 
        password = request.form.get('password')
        print(username)
        print(password)
        # If correct, go to LED control page, otherwise redo
        if username == "Tim" and password == "cowas":
            return redirect(url_for("led_control"))
        else:
            return render_template("login.html", message = "Wrong credentials")
    # GET request
    else:
	    return render_template("login.html")

@app.route("/led/", methods=['GET','POST'])
def led_control():
    if request.method == "POST":
        if request.form.get("Led_toggle") == 'pressed':
            if(g.led_state == 0):
                message = "LED is ON"
                g.led_state = 1
                print("LED 1")
            else:
                message = "LED is OFF"
                g.led_state = 0
                print("LED 0")
                print(g.led_state)

    # GET request
    elif request.method == "GET":
        return render_template("Led_control.html")
    return render_template("Led_control.html", message=message)

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

