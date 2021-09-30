from flask import *
from datetime import datetime
from time import *
from datetime import *
import os
import sqlite3

app = Flask(__name__,template_folder='../KLL_207_ASS3')

 

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
time = str("Current Time =" + current_time)




@app.route("/")

def index():

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    time = str("Current Time =" + current_time)

    return render_template('index.html', data=time) 


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

        current = sqlite3.connect('master.db')

        cur = current.cursor()

        cur.execute("INSERT INTO Users ('Title', 'First Name', 'Last Name', 'Password', 'DOB', 'Country', 'Email')  VALUES ('" + dtitle + "', '"+ dfname +"','"+dlname+"', '"+dpass+"', '"+ddob+"', '"+dcountry+"', '"+demail+"')")

        current.commit()
        current.close()

        return redirect(url_for("index"))
        
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