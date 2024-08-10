import logging
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    create_engine,
    Integer,
    Float,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from support_functions.datetime_format import get_current_time
from typing import List, Optional
from datetime import datetime


class Base(DeclarativeBase):
    pass


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

engine = create_engine("sqlite+pysqlite:///project.db", echo=False)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(16))
    last_name: Mapped[str] = mapped_column(String(16))
    email: Mapped[str] = mapped_column(String(64), unique=True)
    ip_address: Mapped[str] = mapped_column(String(15))
    is_signed_out: Mapped[bool] = mapped_column(Boolean, default=False)
    last_used: Mapped[datetime] = mapped_column(DateTime, default=get_current_time)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    password: Mapped[str] = mapped_column(String(64))
    balance: Mapped[int] = mapped_column(Integer, default=0)

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        ip_address: str,
        is_signed_out: bool = False,
        last_used: datetime = None,
        is_admin: bool = False,
        balance: int = 0,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.ip_address = ip_address
        self.is_signed_out = is_signed_out
        self.last_used = last_used or get_current_time()
        self.is_admin = is_admin
        self.balance = balance


class Brand(Base):
    __tablename__ = "brand"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    models: Mapped[List["Model"]] = relationship("Model", back_populates="brand")

    def __init__(self, name: str):
        self.name = name


class Model(Base):
    __tablename__ = "model"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    brand_id: Mapped[int] = mapped_column(ForeignKey("brand.id"))
    brand: Mapped[Brand] = relationship("Brand", back_populates="models")
    cars: Mapped[List["Car"]] = relationship("Car", back_populates="model")

    def __init__(self, name: str, brand: Brand):
        self.name = name
        self.brand = brand


class Car(Base):
    __tablename__ = "car"
    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brand.id"))
    model_id: Mapped[int] = mapped_column(ForeignKey("model.id"))
    price: Mapped[float] = mapped_column(Float)
    amount: Mapped[int] = mapped_column(Integer)
    brand: Mapped[Brand] = relationship("Brand")
    model: Mapped[Model] = relationship("Model", back_populates="cars")

    def __init__(self, brand: Brand, model: Model, price: float, amount: int):
        self.brand = brand
        self.model = model
        self.price = price
        self.amount = amount


class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))
    date: Mapped[DateTime] = mapped_column(DateTime)
    user: Mapped[User] = relationship("User")
    car: Mapped[Car] = relationship("Car")

    def __init__(self, user: User, car: Car, date: DateTime):
        self.user = user
        self.car = car
        self.date = date


Base.metadata.create_all(engine)
