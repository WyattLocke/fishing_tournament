from fishing_tournament import app
from flask import render_template, redirect, request, session, flash
from fishing_tournament.models.user_model import User
from fishing_tournament.models.submission_model import Submission
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("You must be logged in.", "notinsession")
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    return render_template('dashboard.html', user = User.get_by_id(data), submissions = Submission.get_submissions_by_user_id(data))

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        flash("You must be logged in.", "notinsession")
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    user_in_db = User.get_by_id(data)
    if user_in_db.admin == 'false':
        flash("You are not an administrator", "notinsession")
        return redirect('/')
    return render_template('admin.html', user = User.get_by_id(data))
    # remind me to make sure only the admin can get to admin page

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/registration')
    hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : hash,
        "division" : request.form['division'],
        "guided_unguided" : request.form['guided_unguided'],
        "admin" : 'false'
    }
    user_id = User.register(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    data = {"email" : request.form["email"]}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    if user_in_db.admin == 'true':
        return redirect('/admin')
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@app.route('/verify/<division>/<g_ug>')
def verify_dynamic(division, g_ug):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        "division" : division.capitalize(),
        "guided_unguided" : g_ug.capitalize()
    }

    users = User.get_users_with_submissions_by_division_gu(data)

    return render_template('verify_dynamic.html', users = users)

# test dynamic leaderboard endpoint function
@app.route('/leaderboard/<division>/<g_ug>')
def leaderboard_dyanmic(division, g_ug):
    # logged in user check
    if 'user_id' not in session:
        return redirect('/')

    # data dictionary for query
    data = {
        "division": division.capitalize(),
        "guided_unguided": g_ug.capitalize()
    }

    # query for list of users with max point submissions
    users = User.get_users_with_submissions_scores(data)

    user_data = {
        "id" : session['user_id']
    }

    return render_template('leaderboard_dynamic.html', users=users, user=User.get_by_id(user_data))