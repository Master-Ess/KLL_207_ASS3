from operator import countOf
from os import stat
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Event, User
from . import db


views = Blueprint('views', __name__)

class SpaceShip:
    def __init__(self, name, crew, weight):
        self.name = name
        self.crew = crew
        self.weight = weight

spaceships=[
    SpaceShip('Eagle', 100, 700),
    SpaceShip('Round', 1002, 670),
    SpaceShip('Black Bird', 550, 1000),
    SpaceShip('Seagul', 13, 23400),
    SpaceShip('Pingvin', 200, 12300),
    SpaceShip('Austridge', 500, 11200)
]



@views.route('/', methods=['GET', 'POST'])
def index():
    id = 0
    fname ="Login or Register"
    sname =""
    payload="login"
    if current_user.is_authenticated:
        id = current_user.id
        alldata = User.query.filter_by(id=id).first()
        fname = alldata.first_name
        sname = alldata.last_name
        payload = "edit_account/" + str(id)

    return render_template("index.html", first=fname, second=sname, payload=payload)



@views.route("/book_tickets")
def book_ticket():
    return render_template('book_tickets.html', ships=spaceships)

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
            return render_template("create_event.html", data = "Please fill in all boxes")

        else:
            new_event = Event(title=ename, data=descript, img=URL, status=status, tickets=ntickets, date=DOE, ticketcost=cost, location=location, user_id=cur_user)
            db.session.add(new_event)
            db.session.commit()
            print('Event created or Updated!')
        return render_template('index.html', response='Event created or Updated')
    
    return render_template("create_event.html")

@views.route("/view_event/<id>")
def view_event(id):
    
    alldata = Event.query.filter_by(id=id).first()

    if alldata == None:
        return render_template("404.html")

    name = alldata.title
    location = alldata.location
    date = alldata.date
    tickets = alldata.tickets
    data = alldata.data
    img = alldata.img

    

    return render_template("view_event.html" ,event_name=name , event_location=location ,event_date=date, event_data=data, event_tickets=tickets, event_image=img)

@views.route("/view_previous_purchases")
@login_required
def view_previous_purchases():
    return render_template("view_previous_purchases.html")



@views.route("/edit_account/<id>", methods=['GET', 'POST'])
@login_required
def edit_account(id):
    print(current_user.id)
    if str(current_user.id) != str(id):
        return render_template("403.html")

    alldata = User.query.filter_by(id=id).first()

    if alldata == None:
        return render_template("404.html")

    title = alldata.title
    fname = alldata.first_name
    lname = alldata.last_name
    dateofbirth = alldata.dateofbirth
    country = alldata.country
    email = alldata.email

    return render_template("edit_account.html", title=title, fname=fname, lname=lname, dateofbirth=dateofbirth, country=country, email=email )




