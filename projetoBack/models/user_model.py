from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    senha = Column(String(220), nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, nome='{self.nome}', email='{self.email}')>"