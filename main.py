
from flask import *
from flask_login import LoginManager, UserMixin,login_required,logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from time import *
from datetime import *

import os
import sqlite3

from werkzeug.wrappers import response

User = 0


app = Flask(__name__,template_folder='../KLL_207_ASS3')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


now = datetime.now()

current_time = now.strftime("%H:%M:%S")
time = str("Current Time =" + current_time)



@app.route("/")

def index():

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    time = str("Current Time =" + current_time)

    return render_template('index.html', data=time) 

@app.route("/login", methods=["POST", 'GET'])
def login():
    if request.method == "POST":
        demail= request.form['Username']
        dpassword = request.form['password'] 

        current = sqlite3.connect('master.db')

        cur = current.cursor()

        
        cur.execute("SELECT Password FROM Users WHERE Email = '"+ demail +"'")

        rpassword = cur.fetchall()

        rpassword=str(rpassword)
        rpassword = rpassword.split("'")
        rpassword = rpassword[1]
        dpassword=str(dpassword)

      

        if rpassword != dpassword:
            print("password incorrect")
            return render_template("login.html", response="Email or Password is incorrect")
        elif rpassword == dpassword:
            print("password is correct")

            cur.execute("SELECT UID FROM Users WHERE Email = '"+ demail +"'")

            rUID = str(cur.fetchall())
            rUID = rUID.split("(")
            rUID= str(rUID[1])
            rUID = rUID.split(",")
            rUID= str(rUID[0])
            


        current.close()

        return render_template('index.html', response = "Logged In") 
        
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/book_tickets")
def book_ticket():
    return render_template('book_tickets.html')

@app.route("/make_event")
def make_event():
    return render_template("make_event.html")

@app.route("/view_previous_purchases")
def view_previous_purchases():
    return render_template("view_previous_purchases.html")


@app.route("/create_account", methods=["POST", 'GET'])
def create_account():
    if request.method == "POST":

        dtitle = request.form['usertitle']
        dfname = request.form['fname']
        dlname = request.form['lname']
        ddob = request.form['DOB']
        dcountry = request.form['country']
        demail = request.form['email']
        checkpass1 = request.form['pass']
        checkpass2 = request.form['cpass']

        if checkpass1 == checkpass2:
            dpass = checkpass1
        
        if dtitle == "select" or dfname == None or dlname == None or ddob == None or dcountry == "select" or demail == None or dpass == None:

            return render_template('create_account.html', data = "Please fill in all boxes before entry")
        else:

            current = sqlite3.connect('master.db')

            cur = current.cursor()

            cur.execute("INSERT INTO Users ('Title', 'First Name', 'Last Name', 'Password', 'DOB', 'Country', 'Email')  VALUES ('" + dtitle + "', '"+ dfname +"','"+dlname+"', '"+dpass+"', '"+ddob+"', '"+dcountry+"', '"+demail+"')")

            current.commit()
            current.close()

        return render_template('login.html', response = "Account created, Please login") 
        
    else:
        return render_template('create_account.html')

@app.errorhandler(404)
def page_not_found(e):
    #404 status set explicitly
    return render_template('404.html'), 404

@app.errorhandler(403)    
def page_forbidden(e):
      #403 status set explicitly
    return render_template('403.html'), 403
 

@app.errorhandler(410)    
def page_gone(e):
      #410 status set explicitly
    return render_template('410.html'), 410

@app.errorhandler(500)    
def internal_error(e):
      #500 status set explicitly
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)   