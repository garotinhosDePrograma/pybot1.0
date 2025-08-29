from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func 
from sqlalchemy.orm import relationship
from models.user_model import Base 

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    pergunta = Column(Text, nullable=False)
    resposta = Column(Text, nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now())

    usuarios = relationship("User", backref="logs")

    def __repr__(self):
        return f"<Log(id={self.id}, usuario_id={self.usuario_id}, pergunta='{self.pergunta[:20]}...')>"