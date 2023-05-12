instructions = [
    'SET FOREIGN_KEY_CHECKS=0',
    'DROP TABLE IF EXISTS todo',
    'DROP TABLE IF EXISTS user',
    'SET FOREIGN_KEY_CHECKS=1',
    """
        CREATE TABLE user (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL
        )

    """,
    """
        CREATE TABLE todo (
        id INT PRIMARY KEY AUTO_INCREMENT,
        crated_by INT NOT NULL, 
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL,
        FOREIGN KEY (crated_by) REFERENCES user(id)
        )

    """
]
# Created_by hace una referencia directa a id de la tabla de user

#Para ejecutar el script,  Definir las variables de entorno de nuestro proyecto. Estas ubicadas en __init__ "FLASK_DATABASE_HOST"-
#- Console: export or set FLAS_DATABASE_HOST='localhost'    (for Example) -
#- Con eso ya estaran definidas las variables de entorono dentro de __init__ 

