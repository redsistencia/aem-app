from sqlalchemy.orm import declarative_base

Base = declarative_base() #Crea una clase base.

#Las clases que hereden "Base" serán mapeadas a tablas de la base de datos.