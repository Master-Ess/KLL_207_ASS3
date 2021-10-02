from os import stat
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Event
from . import db


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@views.route("/book_tickets")
def book_ticket():
    return render_template('book_tickets.html')

@views.route("/make_event", methods=['GET', 'POST'])
@login_required
def make_event():
    
    if request.method == 'POST':
        
        ename = request.form.get('eventname')
        ntickets = request.form.get('ntickets')
        status = request.form.get('status')
        DOE = request.form.get('DOE')
        URL = request.form.get('URL')
        cost = request.form.get('cost')
        descript = request.form.get('descript')
        location = request.form.get('location')
        cur_user = str(current_user)
        
        print(descript)
        

        if len(ename) < 1 or len(ntickets) < 1 or len(DOE) < 9 or len(URL) < 1 or len(cost) < 1 or len(status) < 7:
            print("missing errors")
            return render_template("new_create_event.html", data = "Please fill in all boxes")

        else:
            new_event = Event(title=ename, data=descript, img=URL, status=status, tickets=ntickets, date=DOE, ticketcost=cost, location=location, user_id=cur_user)
            db.session.add(new_event)
            db.session.commit()
            print('Event created or Updated!')
        return render_template('index.html', response='Event created or Updated')
    
    return render_template("new_create_event.html")

@views.route("/view_previous_purchases")
@login_required
def view_previous_purchases():
    return render_template("view_previous_purchases.html")



