from flask import *
from datetime import datetime
import re
from time import *
from datetime import *

app = Flask(__name__,template_folder='../KLL_207_ASS3')

 
# currently no operation - now there is 

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
time = str("Current Time =" + current_time)


#index and home functions need to be the same since they are effectivly links to the same page, fix needs to be found

@app.route("/")
def index():
    return render_template('index.html', data=time) 

@app.route("/home")
def home():
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

@app.errorhandler(404)    
def page_not_found(e):
    #404 status set explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)   