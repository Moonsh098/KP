from flask import Blueprint, render_template, request, redirect, url_for, flash, request, flash
from app.models import Customer, Order, LoyaltyPointsHistory, User
from sqlalchemy import and_, func
from datetime import datetime,date
from flask_login import login_user, logout_user, login_required, LoginManager 
from werkzeug.security import check_password_hash
from app.db import db
from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return 'Головна сторінка'


bp = Blueprint('main', __name__)



@bp.route('/clients')
@login_required
def clients():
    customers = Customer.query.all()
    return render_template('clients.html', customers=customers)
@bp.route('/orders')
@login_required
def orders():
    query = Order.query

    # Фільтрація за назвою товару
    product_name = request.args.get('product_name')
    if product_name:
        query = query.filter(Order.product_name.ilike(f"%{product_name}%"))

    # Фільтрація за статусом замовлення
    status = request.args.get('status')
    if status:
        query = query.filter_by(status=status)

    # Фільтрація за датами
    date_from = request.args.get('date_from')
    if date_from:
        query = query.filter(Order.order_date >= date_from)

    date_to = request.args.get('date_to')
    if date_to:
        query = query.filter(Order.order_date <= date_to)

    # Фільтрація за статусом оплати
    payment_status = request.args.get('payment_status')
    if payment_status:
        query = query.filter_by(payment_status=payment_status)

    orders = query.all()
    customers = Customer.query.all()  # Додаємо клієнтів
    return render_template('orders.html', orders=orders, customers=customers)


@bp.route('/')
def home():
    return redirect(url_for('main.login'))


@bp.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        LOYALTY_THRESHOLDS = {
            'Новачок': 0,
            'Лояльний клієнт': 1500,
            'VIP': 5000
        }

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        loyalty_status = request.form['loyalty_status']

        loyalty_status_points = LOYALTY_THRESHOLDS.get(loyalty_status, 0)

        customer = Customer(
            name=name,
            email=email,
            phone=phone,
            address=address,
            loyalty_status=loyalty_status,
            loyalty_status_points=loyalty_status_points,
            loyalty_points=0  # Початкові кешбек-бали
        )

        db.session.add(customer)
        db.session.commit()  # Спочатку треба зберегти, щоб отримати customer.id

        # 👉 Ось тут додаємо запис до історії
        loyalty_history = LoyaltyPointsHistory(
            customer_id=customer.id,
            points=0,
            points_type='Надано статус',
            description=f'Клієнту надано статус "{loyalty_status}" при створенні',
            loyalty_points_before=0,
            loyalty_status_before='Новачок',
            loyalty_status_points_before=0,
            loyalty_points_after=loyalty_status_points,
            loyalty_status_after=loyalty_status,
            loyalty_status_points_after=loyalty_status_points,
            date=datetime.utcnow()
        )
        db.session.add(loyalty_history)
        db.session.commit()

        flash('Клієнта успішно додано', 'success')
        return redirect(url_for('main.clients'))

    return render_template('add_customer.html')


# Сторінка для видалення клієнта
@bp.route('/delete_customer/<int:id>', methods=['GET'])
@login_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('main.clients'))

# Сторінка для редагування клієнта
@bp.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.phone = request.form['phone']
        customer.address = request.form['address']
        customer.loyalty_status = request.form['loyalty_status']
        
        db.session.commit()
        
        return redirect(url_for('main.clients'))
    
    return render_template('edit_customer.html', customer=customer)
    
@bp.route('/add_order', methods=['GET', 'POST'])
@login_required
def add_order():
    customers = Customer.query.all()
    orders = Order.query.all()  # визначаємо одразу
    if request.method == 'POST':
        product_name = request.form['product_name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        customer_id = int(request.form['customer_id'])
        order_date = datetime.strptime(request.form['order_date'], '%Y-%m-%d')
        delivery_type = request.form['delivery_type']
        delivery_address = request.form.get('delivery_address', '') if delivery_type == 'delivery' else ''
        status = request.form['status']
        comment = request.form.get('comment', '')
        payment_status = request.form['payment_status']
        cashback_points = int(request.form['cashbackPoints'])  # Кількість кешбеку для списання

        customer = Customer.query.get(customer_id)

        # Перевіряємо, чи достатньо кешбеку для списання
        if customer.loyalty_points < cashback_points:
            flash('Недостатньо балів кешбеку для списання.', 'danger')
            return redirect(url_for('bp.add_order'))



        # Віднімаємо кешбек від ціни
        discounted_price = price - cashback_points

        # Якщо кешбек зменшує ціну до нуля або менше, встановлюємо ціну на 0
        if discounted_price < 0:
            discounted_price = 0
        order_date_str = request.form['order_date']

        # Додаємо інформацію про кешбек до коментаря, якщо кешбек був використаний
        cashback_comment = f" Оплачено кешбеком: {cashback_points} балів" if cashback_points > 0 else ""
                  # Перетворення рядка дати у об'єкт date
        try:
            order_date = datetime.strptime(order_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Невірний формат дати.", "danger")
            return render_template("orders.html", orders=orders, customers=customers)


        # Перевірка дати
        if order_date > date.today():
                flash("Дата замовлення не може бути в майбутньому.", "danger")
                return render_template("orders.html", orders=orders, customers=customers)


        # Перевірка кількості
        if quantity <= 0:
            flash("Кількість товару має бути більше нуля.", "danger")
            return render_template("orders.html", orders=orders, customers=customers)


        
        # Створюємо нове замовлення
        new_order = Order(
            product_name=product_name,
            quantity=quantity,
            price=discounted_price,  # Змінена ціна після списання кешбеку
            customer_id=customer_id,
            order_date=order_date,
            delivery_type=delivery_type,
            delivery_address=delivery_address,
            status=status,
            comment=f"{comment}{cashback_comment}",  # Додаємо інформацію про кешбек до коментаря
            payment_status=payment_status,
            cashback_used=cashback_points  # Зберігаємо кількість використаного кешбеку
        )
        
        db.session.add(new_order)

        # Списуємо кешбек з клієнта, якщо кількість балів більша за 0
        if cashback_points > 0:
            customer.loyalty_points -= cashback_points

            # Запис в історію про використання кешбеку
            loyalty_points_history = LoyaltyPointsHistory(
                customer_id=customer.id,
                points=-cashback_points,  # Вказуємо негативне значення для списання
                points_type='Зняття балів',
                description=f"Використано кешбек для оплати замовлення {new_order.product_name}",
                loyalty_points_before=customer.loyalty_points + cashback_points,  # До списання
                loyalty_status_before=customer.loyalty_status,
                loyalty_status_points_before=customer.loyalty_status_points,
                loyalty_points_after=customer.loyalty_points,  # Після списання
                loyalty_status_after=customer.loyalty_status,
                loyalty_status_points_after=customer.loyalty_status_points,
                date=datetime.utcnow()
            )

            db.session.add(loyalty_points_history)  # Додаємо до сесії

        db.session.commit()  # Коміт для збереження

        # Якщо оплата підтверджена, нараховуємо бали лояльності
        if customer and payment_status == 'оплачено':
            success = apply_loyalty_logic(new_order, customer)
            if not success:
                return redirect(url_for('bp.add_order'))
    
        db.session.commit()
        flash('Замовлення успішно додано!', 'success')
        return redirect(url_for('main.orders'))
    orders = Order.query.all()  # Додаємо ось це
    return render_template("orders.html", orders=orders, customers=customers)



@bp.route('/delete_order/<int:id>', methods=['POST'])
@login_required
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    flash('Замовлення успішно видалено.', 'success')
    return redirect(url_for('main.orders'))


@bp.route('/edit_order/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    order = Order.query.get_or_404(id)
    old_payment_status = order.payment_status
    old_order_status = order.status

    if request.method == 'POST':
        payment_status = request.form['payment_status']
        status_uk = request.form['status']
        customer = Customer.query.get(order.customer_id)

        # Перевірка: чи потрібно нарахувати бали
        if (
            (old_payment_status != 'оплачено' and payment_status == 'оплачено' and status_uk != 'Скасовано') or
            (old_order_status == 'Скасовано' and status_uk != 'Скасовано' and payment_status == 'оплачено')
        ):
            success = apply_loyalty_logic(order, customer)
            if not success:
                flash('Не вдалося нарахувати бали. Можливо, сталася помилка.', 'danger')
                return redirect(url_for('bp.edit_order', id=id))

        # Перевірка: чи потрібно зняти бали
        if (
            (old_payment_status == 'оплачено' and payment_status != 'оплачено') or
            (old_order_status != 'Скасовано' and status_uk == 'Скасовано')
        ):
            success = apply_loyalty_logic(order, customer, deduct_points=True)
            if not success:
                flash('Не вдалося зняти бали. Можливо, сталася помилка.', 'danger')
                return redirect(url_for('bp.edit_order', id=id))

          
        # Зберігаємо зміни в базі даних для замовлення
        order.payment_status = payment_status
        order.status = status_uk
        db.session.commit()

        flash('Замовлення успішно оновлене!', 'success')
        return redirect(url_for('main.orders'))

    # Для відображення форми редагування замовлення
    customers = Customer.query.all()
    status_choices = ['Очікується', 'Завершено', 'Скасовано']

    return render_template('order.html', order=order, customers=customers, status_choices=status_choices)

@bp.route('/')
def index():
    return render_template('clients.html')




def apply_loyalty_logic(order, customer, loyalty_points=0, deduct_points=False):
    total_price = order.quantity * order.price

        
    if customer.loyalty_status == 'VIP':
        loyalty_status_coeff = 0.06
        loyalty_points_coeff = 0.045
    elif customer.loyalty_status == 'Лояльний клієнт':
        loyalty_status_coeff = 0.03
        loyalty_points_coeff = 0.025
    else:
        loyalty_status_coeff = 0.02
        loyalty_points_coeff = 0.015

    loyalty_status_points = total_price * loyalty_status_coeff
    loyalty_points = total_price * loyalty_points_coeff

    loyalty_points_before = customer.loyalty_points or 0
    loyalty_status_points_before = customer.loyalty_status_points or 0
    loyalty_status_before = customer.loyalty_status
    
    # Логіка для зняття балів кешбеку
    if deduct_points:
        if order.status == 'Скасовано' or order.payment_status != 'Оплачено':
            if customer.loyalty_points >= loyalty_points and customer.loyalty_status_points >= loyalty_status_points:
                customer.loyalty_points -= loyalty_points
                customer.loyalty_status_points -= loyalty_status_points
            else:
                return False  # Якщо недостатньо балів, повертаємо False

            # Запис в історію про зняття балів
            description = f"Замовлення {order.product_name} скасовано або зміна оплати"
            loyalty_points_history = LoyaltyPointsHistory(
                customer_id=customer.id,
                points=-loyalty_points,  # Вказуємо негативне значення для списання
                points_type='Зняття балів',
                description=description,
                loyalty_points_before=loyalty_points_before,
                loyalty_status_before=loyalty_status_before,
                loyalty_status_points_before=loyalty_status_points_before,
                loyalty_points_after=customer.loyalty_points,
                loyalty_status_after=customer.loyalty_status,
                loyalty_status_points_after=customer.loyalty_status_points,
                date=datetime.utcnow()
            )
            db.session.add(loyalty_points_history)  # Додаємо до сесії
            db.session.commit()  # Коміт для збереження
            return True  # Успішно знято бали

    # Логіка для нарахування балів кешбеку
    if not deduct_points:
        customer.loyalty_points += loyalty_points
        customer.loyalty_status_points += loyalty_status_points

    # Оновлення статусу лояльності
    points = float(customer.loyalty_status_points or 0)
    if points >= 5000:
        customer.loyalty_status = 'VIP'
        customer.loyalty_status_points_needed = 0  # Для VIP статусу немає наступного рівня
    elif points >= 1500:
        customer.loyalty_status = 'Лояльний клієнт'
        customer.loyalty_status_points_needed = round(5000 - points)
    else:
        customer.loyalty_status = 'Новачок'
        customer.loyalty_status_points_needed = round(1500 - points)

    # Запис в історію про нарахування балів
    description = (
        f"{'Зняття' if deduct_points else 'Нараховано'} {loyalty_points:.2f} грн за кешбек "
        f"на замовлення {order.product_name}"
    )

    loyalty_points_history = LoyaltyPointsHistory(
        customer_id=customer.id,
        points=-loyalty_points if deduct_points else loyalty_points,
        points_type='Зняття балів' if deduct_points else 'Зарахування балів',
        description=description,
        loyalty_points_before=loyalty_points_before,
        loyalty_status_before=loyalty_status_before,
        loyalty_status_points_before=loyalty_status_points_before,
        loyalty_points_after=customer.loyalty_points,
        loyalty_status_after=customer.loyalty_status,
        loyalty_status_points_after=customer.loyalty_status_points,
        date=datetime.utcnow()
    )

    db.session.add(loyalty_points_history)  # Додаємо до сесії
    db.session.commit()  # Коміт для збереження в базі даних

    return True

@bp.route('/loyalty_dashboard')
@login_required
def loyalty_dashboard():
    # Отримуємо історію балів
    history = LoyaltyPointsHistory.query.order_by(LoyaltyPointsHistory.date.asc(), LoyaltyPointsHistory.id.asc()).limit(100).all()
    history = history[::-1]

    customers = Customer.query.all()
    top_customers_raw = db.session.query(Customer).order_by(Customer.loyalty_points.desc()).limit(5).all()

    # Формуємо топ клієнтів
    top_customers = []
    for customer in top_customers_raw:
        order_count = db.session.query(Order).filter(Order.customer_id == customer.id).count()
        top_customers.append({
            'name': customer.name,
            'loyalty_status_points': customer.loyalty_status_points,
            'loyalty_status': customer.loyalty_status,
            'loyalty_points': customer.loyalty_points,
            'order_count': order_count,
            'points_history': [h.points for h in customer.loyalty_points_history]
        })

    # Дані для графіків
    points_chart = {
        "labels": [entry.date.strftime("%d.%m") for entry in history[-10:]],
        "data": [entry.loyalty_status_points_after for entry in history[-10:]],
    }

    status_chart = {
    "labels": ["VIP", "Лояльний клієнт", "Новачок"],
    "data": [
        sum(1 for c in customers if c.loyalty_status == "VIP"),
        sum(1 for c in customers if c.loyalty_status == "Лояльний клієнт"),
        sum(1 for c in customers if (c.loyalty_status or 'Новачок') == "Новачок"),
    ]
}


    # Формуємо історію балів по клієнтах для вибору в графіку
    points_history_by_customer = {}
    for entry in history:
        customer_id = entry.customer_id
        if customer_id not in points_history_by_customer:
            points_history_by_customer[customer_id] = []
        points_history_by_customer[customer_id].append({
            'date': entry.date.strftime("%d.%m"),
            'points': entry.loyalty_status_points_after
        })

    return render_template(
        'loyalty_dashboard.html',
        history=history,
        customers=customers,
        top_customers=top_customers,
        points_chart=points_chart,
        status_chart=status_chart,
        points_history_by_customer=points_history_by_customer
    )

@bp.route('/test')
def test():
    test_entry = LoyaltyPointsHistory(
        customer_id=1,
        points=100,
        points_type='Зарахування балів',
        description='Тестовий запис',
        loyalty_points_before=0,
        loyalty_status_before='Новачок',
        loyalty_status_points_before=0,
        loyalty_points_after=100,
        loyalty_status_after='Лояльний клієнт',
        loyalty_status_points_after=100,
        date=datetime.utcnow()
    )
    db.session.add(test_entry)
    db.session.commit()
    return 'Тест успішно пройшов'





@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()  # Знайти користувача за логіном
        
        if user and user.check_password(password):  # Перевірка пароля без хешування
            login_user(user)  # Аутентифікація користувача
            return redirect(url_for("main.clients"))  # Перенаправлення на dashboard
        else:
            flash("Невірний логін або пароль", "danger")  # Повідомлення про помилку
            return redirect(url_for("main.login"))  # Перенаправлення назад на сторінку логіну
    
    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вихід успішний", "success")
    return redirect(url_for("main.login"))

from flask_login import current_user

