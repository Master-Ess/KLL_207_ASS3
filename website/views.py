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
        desc = request.form.get('desc')
        location = request.form.get('location')
        cur_user = str(current_user)
        
        
        if ename == None or ntickets == None or status == "Select" or DOE == None or URL == None or cost == None or location == None:
             return render_template("new_create_event.html", data = "Please fill in all boxes")

        
        
        new_event = Event(title=ename, data=desc, img=URL, status=status, tickets=ntickets, date=DOE, ticketcost=cost, location=location, user_id=cur_user)
        db.session.add(new_event)
        db.session.commit()
        print('Event created or Updated!')
        return render_template('index.html', response='Event created or Updated')
    
    return render_template("new_create_event.html")

@views.route("/view_previous_purchases")
@login_required
def view_previous_purchases():
    return render_template("view_previous_purchases.html")

@views.errorhandler(404)
def page_not_found(e):
    #404 status set explicitly
    return render_template('404.html'), 404

@views.errorhandler(403)    
def page_forbidden(e):
      #403 status set explicitly
    return render_template('403.html'), 403
 

@views.errorhandler(410)    
def page_gone(e):
      #410 status set explicitly
    return render_template('410.html'), 410

@views.errorhandler(500)    
def internal_error(e):
      #500 status set explicitly
    return render_template('500.html'), 500
