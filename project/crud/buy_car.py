import os
from sqlalchemy.orm import sessionmaker
from .create_tables import engine, User
from authentication import authorize


def buy_car(current_user: User, session):
    ...
