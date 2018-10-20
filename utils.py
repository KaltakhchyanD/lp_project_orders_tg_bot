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
    orders = relationship('Order', backref = 'customer')

    def __init__(self, full_name = None, email = None, phone_number=None):
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number

    def __repr__(self):
        return f'<User {self.full_name} {self.email} {self.phone_number}>'


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key = True)
    date = Column(DateTime)
    order = Column(Text)
    user_id = Column(ForeignKey('customers.id'))

    def __init__(self, date = None, order = None, user_id = None):
        self.date = date
        self.order = order
        self.user_id = user_id

    def __repr__(self):
        return f'Order {self.id} - {self.order}'


def create_tables():
    Base.metadata.create_all(bind=engine)


def add_customer(full_name, phone_number, email=None):
    c = Customer(full_name, email, phone_number)
    db_session.add(c)
    db_session.commit()


def add_order(order, user_id):
    o = Order(datetime.datetime.now(), order, user_id)
    db_session.add(o)
    db_session.commit()


def get_customer_id_by_phone(phone_number):
    c = Customer.query.filter(Customer.phone_number==phone_number).first()
    return c.id


def get_order_id_by_phone(phone_number):
#    o = Order.query.filter(Order.customer.phone_number==phone_number).first()
    orders = Order.query.all()
    for i in orders:
        if i.customer.phone_number==phone_number:
            return i.id



