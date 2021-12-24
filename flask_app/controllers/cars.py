from flask_app import app
from flask_app.models import user, car
from flask import render_template, redirect, session, request
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)

@app.route('/add_car', methods = ['POST'])
def add_car():
    if not car.Car.validate_info(request.form):
        return redirect('/new')
    car_data = {
        'price': int(request.form['price']),
        'model': request.form['model'],
        'make': request.form['make'],
        'year': int(request.form['year']),
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    new_car = car.Car.add_car(car_data)
    return redirect('/dashboard')

@app.route('/update/<int:car_id>', methods = ['POST'])
def update_car(car_id):
    if not car.Car.validate_info(request.form):
        return redirect('/edit/'+str(car_id))
    car_data = {
        'id': car_id,
        'price': int(request.form['price']),
        'model': request.form['model'],
        'make': request.form['make'],
        'year': int(request.form['year']),
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    edit_car = car.Car.update_car(car_data)
    return redirect('/dashboard')

@app.route('/new')
def new_car():
    return render_template('add_car.html')

@app.route('/show/<int:car_id>')
def show_car(car_id):
    data = {
        'id': car_id
    }
    this_car = car.Car.get_by_id(data)
    return render_template('view_car.html', this_car = this_car)

@app.route('/edit/<int:car_id>')
def edit_car(car_id):
    data = {
        'id': car_id
    }
    this_car = car.Car.get_by_id(data)
    return render_template('edit_car.html', this_car = this_car)

@app.route('/purchase/<int:car_id>/<int:user_id>')
def add_purchase(car_id, user_id):
    data = {
        'car_id': car_id,
        'user_id': session['user_id']
    }
    new_purchase = car.Car.purchase_car(data)
    return redirect('/dashboard')

@app.route('/user/<int:user_id>')
def show_purchases(user_id):
    data = {
        'users_id': user_id
    }
    my_purchases = car.Car.get_purchased_cars(data)
    user_data = {
        'id': session['user_id']
    }
    user_info = user.User.get_by_id(user_data)
    return render_template('my_purchases.html', my_purchases = my_purchases, user_info = user_info)

@app.route('/destroy/<int:car_id>')
def destroy(car_id):
    data = {
        'id': car_id
    }
    this_car = car.Car.destroy(data)
    return redirect('/dashboard')
