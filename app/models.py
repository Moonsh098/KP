from app.db import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
class Customer(db.Model):
    
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    loyalty_status_points = db.Column(db.Float, default=0)  # Бали лояльності
    loyalty_points = db.Column(db.Float, default=0)  # Лояльність поінти (для кешбеку)
    loyalty_status = db.Column(db.String(50), default="Новачок")  # Статус клієнта
    loyalty_points_history = db.relationship('LoyaltyPointsHistory', back_populates='customer')
    orders = db.relationship('Order', backref='customer', lazy=True)


class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_type = db.Column(db.String(50))  # самовивіз або адреса
    delivery_address = db.Column(db.String(200))
    status = db.Column(db.String(50))
    comment = db.Column(db.Text)
    payment_status = db.Column(db.String(50))
    cashback_used = db.Column(db.Integer, nullable=False, default=0)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
  


class LoyaltyPointsHistory(db.Model):
    __tablename__ = 'loyalty_points_history'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='loyalty_points_history')
    points = db.Column(db.Float, nullable=False)
    points_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    loyalty_points_before = db.Column(db.Float, nullable=False)
    loyalty_status_before = db.Column(db.String(50), nullable=False)
    loyalty_status_points_before = db.Column(db.Float, nullable=False)
    loyalty_points_after = db.Column(db.Float, nullable=False)
    loyalty_status_after = db.Column(db.String(50), nullable=False)
    loyalty_status_points_after = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # Додаємо атрибут is_active

    def check_password(self, password):
        return self.password == password