from flask import Blueprint, render_template, request,  redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                print('Logged in successfully!')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
               return render_template("login.html", response = 'Incorrect password, try again.')
        else:
            return render_template("login.html", response = 'Email does not exist.')
    logout_user()
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/create_account', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        title = request.form.get('usertitle')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastname')
        dateofbirth = request.form.get('DOB')
        country = request.form.get('country')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            return render_template("create_account.html", user=current_user, data='Email already exists.')
        elif len(email) < 4:
            return render_template("create_account.html", user=current_user, data='Email must be greater than 3 characters.')
        elif len(first_name) < 2:
            return render_template("create_account.html", user=current_user, data='First name must be greater than 1 character.')
        elif len(last_name) < 2:
            return render_template("create_account.html", user=current_user, data='Last name must be greater than 1 character.')
        elif len(dateofbirth) < 9:
            return render_template("create_account.html", user=current_user, data='Please input a date of birth')         
        elif title == "select":
            return render_template("create_account.html", user=current_user, data='Please Select a Title')
        elif country == "select":
            return render_template("create_account.html", user=current_user, data='Please Select a Country')    
        elif password1 != password2:
            return render_template("create_account.html", user=current_user, data="Passwords don't match.")
        else:
            new_user = User(email=email, title=title, first_name=first_name, last_name=last_name, dateofbirth=dateofbirth, country=country, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            print('Account created!')
            return render_template('index.html', response='Account created and user logged in')

    return render_template("create_account.html", user=current_user)
