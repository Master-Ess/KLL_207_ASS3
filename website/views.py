from operator import countOf
from os import stat
from sre_constants import MARK
from flask import Blueprint, render_template, request, url_for
from flask.wrappers import Response
from flask_login import login_required, current_user
from sqlalchemy import event, update
from werkzeug.utils import redirect
from .models import Event, User, Comment, Purchase
from random import *
from . import db
import re


views = Blueprint('views', __name__)

class IDV_Event:
    def __init__(self, EID, title, location, cost, desc, img, side):
        self.EID = EID
        self.title = title
        self.location = location
        self.cost = cost
        self.desc = desc
        self.img = img
        self.side = side

Levent=[]

class id_purchase:
    def __init__(self, EID, Etitle, Elocation, tickets, cost, date, img):
        self.EID = EID
        self.Etitle = Etitle
        self.Elocation = Elocation
        self.tickets = tickets
        self.cost = cost
        self.date = date
        self.img = img

user_purchases=[]

class eventdisp:
    def __init__(self, CID, Cname, Ccontent, Cside, Cdelete, Cdeletelink):
        self.CID = CID
        self.Cname = Cname
        self.Ccontent = Ccontent
        self.Cside = Cside
        self.Cdelete = Cdelete
        self.Cdeletelink = Cdeletelink

event_comment=[]


@views.route('/', methods=['GET', 'POST'])
def index():

    searched = False
    if request.method == 'POST':
        search = str(request.form.get("search"))
        search = search.lower()
        searched = True

        if search == None:
            searched = False

    

    id = 0
    fname ="Login or Register"
    sname =""
    tpayload="login"
    id = "X"
    if current_user.is_authenticated:
        id = current_user.id
        alldata = User.query.filter_by(id=id).first()
        fname = alldata.first_name
        sname = alldata.last_name
        tpayload = "edit_account/" + str(id)
        id = str(id)
    
    datamaxid = Event.query.count()
    Levent=[]
    i = 1
    s = 1
    print("marker 1")
    
    while i <= datamaxid:
        print("marker 2")
        eventdata = Event.query.filter_by(id=i).first()
        if searched == True:
            print("marker 3")
            x = re.findall(search, eventdata.title.lower())
            y = re.findall(search, eventdata.location.lower())
            z = re.findall(search, eventdata.data.lower())
            
            if(x) or (y) or (z):
                    
                side = "right"
                if (s % 2) == 0:
                    side = "left"
                payload = IDV_Event(i, eventdata.title, eventdata.location, eventdata.ticketcost, eventdata.data , eventdata.img, side)        
                Levent.append(payload)
                s = s + 1
                
            i = i + 1    
        else:
            print("marker 4")
            side = "right"
            if (s % 2) == 0:
                side = "left"
            payload = IDV_Event(i, eventdata.title, eventdata.location, eventdata.ticketcost, eventdata.data , eventdata.img, side)        
            Levent.append(payload)
            s = s + 1
            i = i + 1
        
        



    return render_template("index.html", first=fname, second=sname, payload=tpayload, passevent=Levent)



@views.route("/book_tickets", methods=['GET', 'POST'])
@login_required
def book_ticket():
    
    if request.method == 'POST':

        targetevent= request.form.get('event')
        ntickets = int(request.form.get('ticketno'))       
        cur_user = str(current_user.id)
        eventdata = Event.query.filter_by(id=targetevent).first()
        
        costper = eventdata.ticketcost
        cost = costper * ntickets
        eventmaxtickets = eventdata.tickets
        status = eventdata.status

        if ntickets > eventmaxtickets:
            return render_template("book_tickets.html", response="Please enter a number of tickets that is equal or less than the avalible ammount")
        else:
            if targetevent == "select" or ntickets == None or ntickets < 1:            
                return render_template("book_tickets.html", response = "Please fill in all boxes")

        if status == "Upcomming - TP":
            new_purchase = Purchase(user_id=cur_user,event_id=targetevent,notickets=ntickets,cost=cost)
            db.session.add(new_purchase)
            E = eventdata.tickets
            remaining_tickets = ( int(E) - int(ntickets))
            remaining_tickets_s = str(remaining_tickets)
            eventdata.tickets = remaining_tickets_s
            db.session.commit()
            print('Purchase successful')
            return redirect(url_for('views.index'))
        else:
            return render_template("book_tickets.html", response = "Can't purchase tickets for event at the current time")

        
    else:
        datamaxid = Event.query.count()
        i = 1
        Levent=[]

        while i <= datamaxid:
            eventdata = Event.query.filter_by(id=i).first()
            payload = IDV_Event(i, eventdata.title, eventdata.location, eventdata.ticketcost, "0", "0", "0") #0 = unused parameter so there is no need to actually assing them        
            Levent.append(payload)
            i = i + 1
    
        return render_template('book_tickets.html', passevent=Levent)

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
        cur_user = str(current_user.id)      

        if len(ename) < 1 or len(ntickets) < 1 or len(DOE) < 9 or len(URL) < 1 or len(cost) < 1 or len(status) < 7:
            print("missing errors")
            return render_template("create_event.html", data = "Please fill in all boxes")

        else:
            new_event = Event(title=ename, data=descript, img=URL, status=status, tickets=ntickets, date=DOE, ticketcost=cost, location=location, user_id=cur_user)
            db.session.add(new_event)
            db.session.commit()
            print('Event created or Updated!')
        return redirect(url_for('views.index'))
    
    return render_template("create_event.html" , delete="invis", status="Select")

@views.route("/view_event/<id>", methods=['GET', 'POST'])
def view_event(id):
    if request.method == 'POST':
        if current_user.is_authenticated:
            cdata = request.form.get('descript')
            print(cdata)
            print('marker')
            EID = id
            UID = current_user.id

            new_comment = Comment(user_id=UID, event_id=EID, data=cdata)
            db.session.add(new_comment)
            db.session.commit()
        else:
            return render_template("login.html")

    editdata = ""

    alldata = Event.query.filter_by(id=id).first()
    if current_user.is_authenticated:
        if int(current_user.id) == int(alldata.user_id):
            editdata = "Edit Event"

    if alldata == None:
        return render_template("404.html")

    name = alldata.title
    location = alldata.location
    date = alldata.date
    tickets = alldata.tickets
    data = alldata.data
    img = alldata.img
    status = alldata.status

    get = Comment.query.filter(Comment.event_id == id).order_by(Comment.id.desc()).first()
    datamaxid = 0
    if get != None:
        datamaxid = get.id

    i = 1
    x = 1
    event_comment=[]
    
    while i <= datamaxid:
        commentdata = Comment.query.filter_by(id  = i).first()
        if commentdata != None:
            cdelete = ""
            cdeletelink = ""

            
            if int(commentdata.event_id) == int(id):
                userdata = User.query.filter_by(id=commentdata.user_id).first()
                side = "cleft"
                if (x % 2) == 0:
                    side = "cright"
                if current_user.is_authenticated:
                    if current_user.id == userdata.id:
                        cdelete = "DELETE"
                        cdeletelink = "delete/" + str(i) + "/" + str(id)
                    
                payload = eventdisp(userdata.id, userdata.first_name , commentdata.data, side, cdelete, cdeletelink)   
                event_comment.append(payload)
                x = x + 1 
            
        i = i + 1

    return render_template("view_event.html" ,event_name=name , event_location=location ,event_date=date, event_data=data, event_tickets=tickets, event_image=img, edit=editdata, status=status, id=id, passcomment=event_comment)

@views.route("/view_previous_purchases")
@login_required
def view_previous_purchases():   
    id = 'x'
    id = current_user.id
    if str(current_user.id) != str(id):
        return render_template("403.html")

    email = current_user.email
    

    datamaxid = Purchase.query.filter(Purchase.user_id == id).count()
    print(datamaxid)
    if datamaxid == 0:
        return render_template("view_previous_purchases.html", email = email, response="User has not purchased any tickets")
    
    
    i = 1
    user_purchases=[]

    while i <= datamaxid:
        
        purchasedata = Purchase.query.filter_by(id=i).first()
        eventdata = Event.query.filter_by(id = purchasedata.event_id).first()
        
        if int(purchasedata.user_id) == int(id):
            
            payload = id_purchase(purchasedata.event_id, eventdata.title, eventdata.location, purchasedata.notickets, purchasedata.cost, purchasedata.purchasedate, eventdata.img)        
            user_purchases.append(payload)
            
        i = i + 1
    
        #return render_template('book_tickets.html', passevent=Levent)

    return render_template("view_previous_purchases.html", email = email, passpurchase=user_purchases)



@views.route("/edit_account/<id>", methods=['GET', 'POST'])
@login_required
def edit_account(id):

    if request.method == 'POST':
        alldata = User.query.filter_by(id=id).first()

        #if you submit a NONE it freaks out so you gotta do a bunch of shit like this, i could probably write a def to do it but i cbf
        value = request.form.get('title')
        if value != None:
            alldata.title = value
            db.session.commit() 

        value = request.form.get('fname')
        if value != None:
            alldata.first_name = value
            db.session.commit()  

        value = request.form.get('lname')
        if value != None:
            alldata.last_name = value
            db.session.commit()          

        value = request.form.get('DOB')
        if value != None:
            alldata.dateofbirth = value
            db.session.commit() 

        value = request.form.get('Country')
        if value != None:
            alldata.country = value
            db.session.commit()  

        value = request.form.get('email')
        if value != None:
            alldata.email = value
            db.session.commit()   

        return redirect(url_for('views.index'))

    else:

        
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

@views.route("/make_event/<id>", methods=['GET', 'POST'])
@login_required
def edit_event(id):
    if request.method == 'POST':
        
        alldata = Event.query.filter_by(id=id).first()

        value = request.form.get('eventname')
        if value != None:
            alldata.title = value
            db.session.commit() 

        value = request.form.get('ntickets')
        if value != None:
            alldata.tickets = value
            db.session.commit()  

        value = request.form.get('status')
        if value != None:
            alldata.status = value
            db.session.commit()          

        value = request.form.get('DOE')
        if value != None:
            alldata.date = value
            db.session.commit() 

        value = request.form.get('URL')
        if value != None:
            alldata.img = value
            db.session.commit()  

        value = request.form.get('cost')
        if value != None:
            alldata.ticketcost = value
            db.session.commit()

        value = request.form.get('location')
        if value != None:
            alldata.location = value
            db.session.commit()
        
        value = request.form.get('descript')
        if value != None:
            alldata.data = value
            db.session.commit()
           

        return redirect(url_for('views.index'))  

        
    else:
        alldata = Event.query.filter_by(id=id).first()


        if alldata == None:
            return render_template("404.html")

        if str(current_user.id) != str(alldata.user_id):
            return render_template("403.html")


        name = str(alldata.title)
        id = alldata.id
        tickets = alldata.tickets
        status = alldata.status
        DOE = alldata.date
        location = alldata.location
        URL = alldata.img
        cost = alldata.ticketcost
        desc = alldata.data

        return render_template("create_event.html", name=name, tickets=tickets, status=status, DOE=DOE, location=location, URL=URL, cost=cost, desc=desc, id = id)

@views.route("/make_event/delete/<id>", methods=['GET', 'POST'])
@login_required
def delete_event(id):

    alldata = Event.query.filter_by(id=id).first()


    if alldata == None:
        return render_template("404.html")

    if str(current_user.id) != str(alldata.user_id):
        return render_template("403.html")

    Event.query.filter_by(id=id).delete()
    print('EVENT DELETED')
    db.session.commit()

    return redirect(url_for('views.index'))

@views.route("/view_event/delete/<id>/<adr>")
@login_required
def delete_comment(id,adr):

    alldata = Comment.query.filter_by(id=id).first()


    if alldata == None:
        return render_template("404.html")

    if str(current_user.id) != str(alldata.user_id):
        return render_template("403.html")

    Comment.query.filter_by(id=id).delete()
    print('COMMENT DELETED')
    db.session.commit()
    link = "/view_event/" + str(adr)

    return redirect( link , code = 302)