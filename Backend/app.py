from flask import Flask,render_template, request,redirect,url_for,session
from forms import LoginForm

app = Flask(__name__, 
            template_folder='../Frontend/templates', 
            static_folder='../Frontend/static')

app.secret_key = "nutrition_secret_key"


USER_EMAIL = "himanshubora100@gmail.com"
USER_PASSWORD = "12345678"



@app.route("/",methods=["GET","POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if(form.email.data==USER_EMAIL and form.password.data == USER_PASSWORD):
            session["user"] = form.email.data
            return redirect(url_for("home"))
        else:
            return render_template("login.html",form = form, error = "INvalid Email or Password")
        
    return render_template("login.html",form = form)

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    
    return render_template("home.html",user = session["user"])


@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)