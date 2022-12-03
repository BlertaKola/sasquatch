from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.sighting import Sighting
from flask_app.models.user import User



@app.route('/new/sighting')
def newReport():
    if 'user' not in session:
        return redirect('/')
    data = {
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data)
    return render_template("addReport.html", loggedUser = loggedUser)

    
@app.route('/reportform', methods = ['POST'])
def addReportForm():
    if not Sighting.validateReport(request.form):
        flash("Something is wrong, check the errors", 'reportError')
        return redirect(request.referrer)
    data = {
        'location': request.form['location'],
        'description': request.form['description'],
        'dateSight': request.form['dateSight'],
        'numberSasq': request.form['numberSasq'],
        'user_id': session['user']
    }
    Sighting.addReport(data)
    return redirect('/dashboard')


@app.route('/edit/<int:id>')
def editReport(id):
    if 'user' not in session:
        return redirect('/dashboard')
    data = {
        'sighting_id': id,
        'user_id': session['user']
    }
    currentSight = Sighting.getReportByID(data)
    if not session['user'] == currentSight['user_id']:
        return redirect('/404Error')

    sighting = Sighting.getReportByID(data)
    loggedUser = User.getUserByID(data)
    return render_template("editReport.html", loggedUser = loggedUser, sighting = sighting)


@app.route('/editForm/<int:id>', methods = ['POST'])
def editForm(id):
    if 'user' not in session:
        return redirect('/logout')
    if not Sighting.validateReport(request.form):
        flash("Something is wrong, check the errors", 'reportError')
        return redirect(request.referrer)
    data = {
        'id': id,
        'location': request.form['location'],
        'description': request.form['description'],
        'dateSight': request.form['dateSight'],
        'numberSasq': request.form['numberSasq'],
        'user_id': session['user']
    }
    Sighting.updateReport(data)
    return redirect('/dashboard')

@app.route('/404Error')
def error():
    return render_template("404Error.html")


@app.route('/delete/<int:id>')
def delete(id):
    data = {
        'sighting_id': id,
        'user_id': session['user']
    }

    currentSight = Sighting.getReportByID(data)
    print(currentSight)
    if not session['user'] == currentSight['user_id']:
        return redirect('/404Error')

    Sighting.deleteReport(data)
    Sighting.deleteBelievers(data)
    return redirect(request.referrer)


@app.route('/view/<int:id>')
def viewReport(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'sighting_id': id,
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data)
    sighting = Sighting.getReportByID(data)
    sceptics = Sighting.getSceptics(data)
    believers = Sighting.believUnbelieve(data)
    return render_template("viewReport.html", loggedUser = loggedUser, sighting = sighting, believers = believers, sceptics =sceptics)


@app.route('/believe/<int:id>')
def believe(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'sighting_id': id,
        'user_id': session['user']
    }
    Sighting.believeReport(data)
    return redirect(request.referrer)


@app.route('/unbelieve/<int:id>')
def unbelieve(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'sighting_id': id,
        'user_id': session['user']
    }
    Sighting.unbelieveReport(data)
    return redirect(request.referrer)