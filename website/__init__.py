from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask import render_template

db = SQLAlchemy()
DB_NAME = "master.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'kenzie-luke-leianna'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views, persistant_usr
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Event

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

   
    @app.errorhandler(404)
    def page_not_found(e):
    #404 status set explicitly
        return render_template('404.html', pers=persistant_usr), 404

    @app.errorhandler(403)    
    def page_forbidden(e):
      #403 status set explicitly
        return render_template('403.html', pers=persistant_usr), 403
 

    @app.errorhandler(410)    
    def page_gone(e):
      #410 status set explicitly
        return render_template('410.html', pers=persistant_usr), 410

    @app.errorhandler(500)    
    def internal_error(e):
      #500 status set explicitly
        return render_template('500.html', pers=persistant_usr), 500


    return app

    

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')
