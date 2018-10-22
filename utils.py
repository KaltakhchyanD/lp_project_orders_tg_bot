import datetime
from email.message import EmailMessage
import smtplib
import os

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import psycopg2


def send_mail(txt_2_send, dst):
    src = os.getenv('EMAIL_FROM')
    pswd = os.getenv('PSWD')
    s = smtplib.SMTP('smtp.yandex.ru', 587)
    s.starttls()
    s.login(src, pswd)
    msg = EmailMessage()
    msg.set_content(txt_2_send)
    msg['Subject'] = 'New order'
    msg['From'] = src
    msg['To'] = dst
    s.send_message(msg)
    s.quit()


engine = create_engine('postgresql+psycopg2://daniel:some_password@localhost:5432/test_db')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    full_name=Column(String(50))
    email=Column(String(100), unique=True)
    phone_number=Column(String(100), unique=True)
    tg_chat_id=Column(Integer)
    orders = relationship('Order', backref = 'customer')

    def __init__(self, full_name = None, phone_number=None, tg_chat_id=None, email = None):
        self.full_name = full_name
        self.phone_number = phone_number
        self.tg_chat_id = tg_chat_id
        self.email = email

    def __repr__(self):
        return f'<User {self.full_name} {self.email} {self.phone_number}>'



class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key = True)
    date = Column(DateTime)
    order = Column(Text)
    user_id = Column(ForeignKey('customers.id'))
    pizza = relationship('Association', backref = 'order')
    drink = relationship('Association_drinks', backref='order')

    def __init__(self, date = None, order = None, user_id = None):
        self.date = date
        self.order = order
        self.user_id = user_id

    def __repr__(self):
        return f'Order {self.id} - {self.order}'


class Pizza(Base):
    __tablename__ = 'pizzas'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100), unique = True)
    price = Column(Integer)
    order = relationship('Association', backref = 'pizza')

    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def __repr__(self):
        return f'Pizza {self.name}: {self.price}'


class Drink(Base):
    __tablename__ = 'drinks'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100), unique = True)
    price = Column(Integer)
    order = relationship('Association_drinks', backref = 'drink')

    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def __repr__(self):
        return f'Drink {self.name}: {self.price}'


class Association(Base):
    __tablename__='association'
    order_id = Column(ForeignKey('orders.id'), primary_key=True)
    pizza_id = Column(ForeignKey('pizzas.id'), primary_key=True)
    extra_data = Column(String(100))


class Association_drinks(Base):
    __tablename__='association_drinks'
    order_id = Column(ForeignKey('orders.id'), primary_key=True)
    drink_id = Column(ForeignKey('drinks.id'), primary_key=True)
    extra_data = Column(String(100))


def create_tables():
    Base.metadata.create_all(bind=engine)


def add_customer(full_name, phone_number, tg_chat_id, email=None):
    c = Customer(full_name, phone_number, tg_chat_id, email)
    db_session.add(c)
    db_session.commit()


def add_order(order, user_id):
    o = Order(datetime.datetime.now(), order, user_id)
    db_session.add(o)
    db_session.commit()


def get_customer_id_by_phone(phone_number):
    c = Customer.query.filter(Customer.phone_number==phone_number).first()
    if not c:
        return False
    return c.id


def get_order_id_by_phone(phone_number):
    #o = Order.query.filter(Order.customer.phone_number==phone_number).first()
    orders = Order.query.all()
    for i in orders:
        if i.customer.phone_number==phone_number:
            return i.id


def get_pizza_by_id(id):
    pizza = Pizza.query.filter(Pizza.id==id).first()
    if not pizza:
        return False
    return pizza


def pizza_names_for_regex_hendler():
    pizza_names = [line.name for line in Pizza.query.all()]
    string_of_names = "|".join(pizza_names)
    return string_of_names


