# ----------------------------------------------------------------------- #     
#                                                                         #
#   DocAux - Models module
#          Description: This is where all the database stuff is handeled
# ----------------------------------------------------------------------- #     

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

# This initializes the base classes, Its silly but this is needed.
class Base(MappedAsDataclass, DeclarativeBase):
    pass

# This can be imported
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "Test_Users"
    id: Mapped[int] = db.mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username