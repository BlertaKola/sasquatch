from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from flask_app.models.sighting import Sighting
from flask_app.models.user import User


@app.route('/')
def loginPage():
    return render_template("loginRegister.html")


@app.route('/registerUser', methods = ['POST'])
def registerUser():
    if not User.validateUser(request.form):
        flash("Something is wrong, check the errors", 'signUpError')
        return redirect(request.referrer)
    if User.getUserByEmail(request.form):
        flash("This email already exists, try another one", 'emailRegister')
        return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.addUser(data)
    flash("You can now login", 'signUpSuccess')
    return redirect(request.referrer)

@app.route('/loginUser', methods = ['POST'])
def loginUser():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    if len(request.form['email'])< 1:
        flash("Please enter the email", 'emailLogin')
        return redirect(request.referrer)
    if not User.getUserByEmail(data):
        flash("This email doesn't exit, try again", 'emailLogin')
        return redirect(request.referrer)
    user = User.getUserByEmail(data)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Incorrect password", 'passwordLogin')
        return redirect(request.referrer)
    
    session['user'] = user['id']
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    sceptics = Sighting.getScepticsCount(data)
    loggedUser = User.getUserByID(data)
    sightings = Sighting.getAllReports()
    return render_template("dashboard.html", loggedUser = loggedUser, sightings = sightings, sceptics = sceptics)



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
