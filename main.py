from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, session
from flask_wtf import CSRFProtect
from flask_oauthlib.client import OAuth




app = Flask(__name__)
app.config['SECRET_KEY'] = "bla"
app.config['GOOGLE_ID'] = "bla"
app.config['GOOGLE_SECRET'] = "bla"
csrf = CSRFProtect(app)
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key = app.config['GOOGLE_ID'],
    consumer_secret= app.config['GOOGLE_SECRET'],
    request_token_param= {
        'scope': 'email'
    },
    base_url= 'https://googleapis.com/oath2/v1',
    request_token_url = None,
    access_token_method = 'POST',
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    authorize_url = 'https://accounts.google.com/o/oauth2/auth'
)

@app.route("/assets/style.css")
def styles():
    return send_from_directory("assets","style.css")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/podjetja")
def podjetja():
    return render_template("podjetja.html")

@app.route("/komentarji")
def komentarji():
    return render_template("komentarji.html")

@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "valid_username" and password == "valid_password":
            flash("Login succesful", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "error")
            
    return redirect(url_for("index"))

@app.route("/register", methods= ["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        birthdate = request.form.get("birthdate")
        username = request.form.get("username")
        password = request.form.get("password")

        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/login/google")
def login_google():
    return google.authorize(callback=url_for('authorized', external = True ))

@app.route("/logout")
def logout():
    session.pop('google_token', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('acces_token') is None:
        flash('Acces Denied: reason: {} error = {}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('login'))
    
    session['google_token'] = (response['acces_token'], '')
    user_info = google.get('userinfo')
    flash('logged in as: ' + user_info.data['email'])
    return redirect(url_for('index'))

@google.tokengetter
def get_google_oath_token():
    return session.get('google_token')

@app.route("/static/css/style.css")
def styles_of():
    return send_from_directory("static/css", "style.css")

@app.route("/static/images/xxplogo.svg")
def image_use():
    return send_from_directory("static/assets/images", "xxplogo.svg")

if __name__ == "__main__":
    app.run(port="5001", use_reloader = True)

