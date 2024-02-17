from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import DeclarativeBase

class Base(MappedAsDataclass, DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)