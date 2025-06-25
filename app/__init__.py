from flask import Flask
from app.db import db  # Імпортуємо db з db.py
from app.routes import bp  # Імпортуємо маршрути
from flask_login import LoginManager
from app.routes import bp as routes_bp

login_manager = LoginManager()
login_manager.login_view = 'main.login'  # або 'login' — перевір ім’я функції
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

delivery_status_map = {
    'Pending': 'Очікується',
    'Shipped': 'Відправлено',
    'Delivered': 'Доставлено'
}



def create_app():
    app = Flask(__name__)
    app.secret_key = 'key123'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root098@localhost/clients'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['LOGIN_URL'] = '/login'
    db.init_app(app)
    login_manager.init_app(app)
 

    # ✅ Реєстрація фільтрів всередині create_app
    @app.template_filter('translate_delivery_type')
    def translate_delivery_type(delivery_type):
        return delivery_type_map.get(delivery_type, delivery_type)

    @app.template_filter('translate_status')
    def translate_status(status):
        return status_map.get(status, status)

    @app.template_filter('translate_order_status')
    def translate_order_status(status):
        return delivery_status_map.get(status, status)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    with app.app_context():
        db.create_all()

    return app
