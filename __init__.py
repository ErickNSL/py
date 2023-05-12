import os
from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_mapping( #Configuracion de variables
        SECRET_KEY='mikey', #Definira el inicio de secion mediante cookis 
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),            #|
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),    #| Se usara despues cuando definamos los accesos a la base de datos.
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),            #|
        DATABASE=os.environ.get('FLASK_DATABASE'),                       #|
    )

    from . import db
    from . import auth

    db.init_app(app)
    app.register_blueprint(auth.bp)

    @app.route('/hola')
    def hola():
        return "Hola putitas"
    
    return app
        