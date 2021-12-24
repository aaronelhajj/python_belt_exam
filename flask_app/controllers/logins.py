from flask_app import app
from flask_app.models import user, car
from flask import render_template, redirect, session, request
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['POST'])
def register():
    if not user.User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    print(data)
    user_id = user.User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = user.User.get_by_email(data)
    
    if not user_in_db:
        flash("Invalid Email", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Password', 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    data = {
        'id': session['user_id']
    }
    user_info = user.User.get_by_id(data)
    all_cars = car.Car.get_all()
    return render_template('dashboard.html', user_info = user_info, all_cars = all_cars)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')