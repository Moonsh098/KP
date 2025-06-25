from flask import Flask, render_template
from db import db

from models import Customer, Order

from flask_login import LoginManager

# Ініціалізація LoginManager


# Мапи для перекладу статусів
status_map = {
    'Очікується': 'Pending',
    'Завершено': 'Completed',
    'Скасовано': 'Cancelled'
}

delivery_type_map = {
    'pickup': 'Самовивіз',
    'delivery': 'Доставка'
}

# Мапа для статусів замовлення
delivery_status_map = {
    'Pending': 'Очікується',
    'Shipped': 'Відправлено',
    'Delivered': 'Доставлено'
}




