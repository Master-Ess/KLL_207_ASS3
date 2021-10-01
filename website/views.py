from flask import Blueprint, render_template, request, flash, jsonify
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

@views.route("/make_event")
def make_event():
    return render_template("make_event.html")

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
