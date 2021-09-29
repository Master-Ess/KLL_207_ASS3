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

@app.route("/")
def index():
    return render_template('index.html', data=time)


@app.route("/book_tickets")
def book_ticket():
    return render_template('events/book_tickets.html')

@app.route("/make_event")
def make_event():
    return render_template("make_event.html")

@app.route("/view_previous_purchases")
def view_previous_purchases():
    return render_template("view_previous_purchases.html")

@app.route("/article/meet_the_drivers")
def meet_the_drivers():
    return render_template("events/meet_the_drivers.html")

@app.route("/article/streets_of_monza_event")
def meet_the_drivers():
    return render_template("events/streets_of_monza_event.html")

@app.route("/article/subsonica_preformance")
def meet_the_drivers():
    return render_template("events/subsonica_preformance.html")

if __name__ == "__main__":
    app.run(debug=True)   