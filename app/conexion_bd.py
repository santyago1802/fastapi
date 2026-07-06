from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine

nombre_bd = "bd_clientes.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

#motor de base de datos
motor_bd = create_engine(url_bd)

# definir el metodo para crer las tablas 

def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield


# definir el metodo para la sesion

def obtener_session():
    with Session(motor_bd) as mi_session:
        yield mi_session

# denominado inyeccion de dependencias
#registrar la sesion como dependencia
Session_dependencia = Annotated[Session, Depends(obtener_session)]