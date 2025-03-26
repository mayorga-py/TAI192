import os 
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

dbNAME = 'usuarios.sqlite' #asignar el nombre de la base de datos
base_dir = os.path.dirname(os.path.realpath(__file__)) #para que la bd se cree sobre la misma carpeta del archivo
dbURL = f'sqlite:///{os.path.join(base_dir,dbNAME)}' #ruta de la base de datos

engine=create_engine(dbURL,echo=True) #crear motor de base de datos
Session = sessionmaker(bind=engine) #crear sesion
Base = declarative_base() #crear base de datos, y tmb hacemos la conexion con la base de datos
#con esto si no hay una base de datos, se creara una nueva y si ya existe lo ignorara



