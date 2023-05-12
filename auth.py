#Modulos de autenticacion en flask es una grupacion de modulos que hacen sentido. si se va tener un modulo de autenticacion o blueprint. lo que tine
#mas sentido es que tenga, inicio de sesion, autenticacion. etc. el firewall nos perimite bloquear a quienens no tengan autorizacion o inicio de secion etc.
import functools #Set de funciones para construir a pps

from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
from werkzeug.security import check_password_hash, generate_password_hash #CH, verifica si la contraseña es igual a otra. GE, encrypta la contraseña

from todo.db import get_db
#blue print: Añadir blueprints configurables.
#flash: Permitir enviar mensajes de manera directa a nuestras platillas. como por ejemplo error de inicio de sesion
#render_template: para renderizar platillas html
#session: para mantener una referencia del usuario interactuando con la app 

bp = Blueprint('auth', __name__, url_prefix='/auth')#Lo que hara url_prefix es concatenar con las otras url que vayamos creando. Example"/auth/register"

#Para crear una ruta de bp es bastante similar a crear una ruta con flask, solo que usaremos bp.route en vez de app.route



###### REGISTER ######
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
             'select id from user where username = %s', (username,)
        )

        if not username:
            error = "Username is required"

        if not password:
            error = "Password is required"

        elif c.fetchone() is not None:
            error = "User {} is already register".format(username)

        if error is None:
            c.execute(
                'insert into user (username, password) values (%s, %s)',
                (username, generate_password_hash(password))
            )
            db.commit()

            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


####### LOGIN #####
@bp.route('/login', methods =['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select * from user where username = %s', (username,)
        )
        user = c.fetchone

        if user is None:
            error = "invalid password and/or user"
        elif not check_password_hash(user['password'], password):
            error = "invalid password and/or user"
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')

