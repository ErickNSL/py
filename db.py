import mysql.connector

import click
from flask import current_app, g #Cuurent, mantiene la aplicacion que estamos ejecutando. g, es una variable que se encuentra en toda nuestra app
from flask.cli import with_appcontext #Serivra cuando ejecutemos db scrip. ya que necistarmos el contexto, accediendo a las variables de la appp
from .schema import instructions


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(     #Se le dara una nueva propiedad a g, que contiene...
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c



### Cerrar la coneccion a la base de datos despues de cada peticion.

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db, c = get_db()

    for i in instructions: #MySql solo un commando. Solucion, iterar entre las instruciones de .schema
        c.execute(i)
    
    db.commit()

@click.command('initdb')#Nombre, nos servira cuando querramos llamarlo en la terminal (console: flask init-db)= Ejecuta la funcion. 
@with_appcontext #Necesita contexto de la app, para que pueda acceder a las variables de la configuracion "DATABASE_USER etc..".
def init_db_command(): 
    init_db()#Se encargara de correr la logica de los scripts que nosotros definamos
    click.echo("Database inizalized")


def init_app(app): # Se tiene que pedir el argumento de app
    app.teardown_appcontext(close_db)#Suscribiendo "init_db_commmand" a nuestra aplicacion
    app.cli.add_command(init_db_command)


