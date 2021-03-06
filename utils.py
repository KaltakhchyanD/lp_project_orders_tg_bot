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

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/{db_name}')
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
    address_id = Column(ForeignKey('addresses.id'))
    pizza = relationship('Association_pizzas', backref = 'order')
    drink = relationship('Association_drinks', backref='order')

    def __init__(self, date = None, order = None, user_id = None, address_id = None):
        self.date = date
        self.order = order
        self.user_id = user_id
        self.address_id = address_id

    def __repr__(self):
        return f'Order {self.id} - {self.order} at {self.address_id}'

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key = True)
    coords = Column(String(200))
 #   lat = Column(String(100))
 #   lon = Column(String(100))
    address = Column(String(100))
    address_details = Column(String(100))
    orders = relationship('Order', backref = 'address')

    def __init__(self, coords = None, address = None, address_details = None):
        self.coords = coords
#        self.lat = lat
#        self.lon = lon
        self.address = address
        self.address_details = address_details

    def __repr__(self):
        return f'Coords - {self.coords}, Address_full - {self.address}, {self.address_details}'



class Pizza(Base):
    __tablename__ = 'pizzas'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100), unique = True)
    price = Column(Integer)
    order = relationship('Association_pizzas', backref = 'pizza')

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


class Association_pizzas(Base):
    __tablename__='association_pizzas'
    order_id = Column(ForeignKey('orders.id'), primary_key=True)
    pizza_id = Column(ForeignKey('pizzas.id'), primary_key=True)
    how_many_in_order = Column(Integer)
    
    def __init__(self, order_id, pizza_id, how_many_in_order):
        self.order_id = order_id
        self.pizza_id = pizza_id
        self.how_many_in_order = how_many_in_order

    def __repr__(self):
        return f'Association Order {self.order_id} : Pizza {self.pizza_id}'


class Association_drinks(Base):
    __tablename__='association_drinks'
    order_id = Column(ForeignKey('orders.id'), primary_key=True)
    drink_id = Column(ForeignKey('drinks.id'), primary_key=True)
    how_many_in_order = Column(Integer)
    
    def __init__(self, order_id, drink_id, how_many_in_order):
        self.order_id = order_id
        self.drink_id = drink_id
        self.how_many_in_order = how_many_in_order

    def __repr__(self):
        return f'Association Order {self.order_id} : Drink {self.drink_id}'


def create_tables():
    Base.metadata.create_all(bind=engine)


def add_customer(full_name, phone_number, tg_chat_id, email=None):
    c = Customer(full_name, phone_number, tg_chat_id, email)
    db_session.add(c)
    db_session.commit()


def add_address(coords, address, address_details):
    a = Address(coords, address, address_details)
    db_session.add(a)
    db_session.commit()


def add_order(order, user_id, address_id, *products):
    order = Order(datetime.datetime.now(), order, user_id, address_id)
    db_session.add(order)
    db_session.commit()
    product_names = [i.name for i in products]
    #g = db_session.query(Association.query.filter(Association.order_id == 15, Association.pizza_id == 1).exists()).scalar()
    for product_name in set(product_names):
        add_product_to_assciation_table(order, get_product_by_name(product_name), product_names.count(product_name))


def get_customer_by_phone(phone_number):
    customer = Customer.query.filter(Customer.phone_number==phone_number).first()
    if not customer:
        return False
    return customer


def get_address_by_coords_db(coords):
#    str_coords = ', '.join([i for i in coords])
    address = Address.query.filter(Address.coords==coords).first()
    if not address:
        return False
    return address


def get_order_by_phone(phone_number):
    orders = Order.query.all()
    for i in orders:
        if i.customer.phone_number==phone_number:
            return i


def get_pizza_by_id(id):
    pizza = Pizza.query.filter(Pizza.id==id).first()
    if not pizza:
        return False
    return pizza


def get_pizza_by_name(name):
    pizza = Pizza.query.filter(Pizza.name==name).first()
    if not pizza:
        return False
    return pizza


def get_drink_by_name(name):
    drink = Drink.query.filter(Drink.name==name).first()
    if not drink:
        return False
    return drink


def get_product_by_name(product_name):
    if get_pizza_by_name(product_name):
        return get_pizza_by_name(product_name)
    elif get_drink_by_name(product_name):
        return get_drink_by_name(product_name)
    else:
        return False


def get_drink_by_id(id):
    drink = Drink.query.filter(Drink.id==id).first()
    if not drink:
        return False
    return drink


def pizza_names_for_regex_hendler():
    pizza_names = [line.name for line in Pizza.query.all()]
    string_of_names = "|".join(pizza_names)
    return string_of_names


def drink_names_for_regex_hendler():
    drink_names = [line.name for line in Drink.query.all()]
    string_of_names = "|".join(drink_names)
    return string_of_names


def add_product_to_assciation_table(order, product, count):
    if isinstance(product, Pizza):
        association = Association_pizzas(order.id, product.id, count)
    elif isinstance(product, Drink):
        association = Association_drinks(order.id, product.id, count)
    else:
        return False # Might be good idea to raise some custom exception
    db_session.add(association)
    db_session.commit()

