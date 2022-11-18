from fishing_tournament import app
from flask import render_template, redirect, request, session, flash
from fishing_tournament.models.submission_model import Submission
from fishing_tournament.models.user_model import User

@app.route('/submission')
def submission():
    if 'user_id' not in session:
        flash("You must be logged in.", "notinsession")
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    return render_template('submission.html', user = User.get_by_id(data))

@app.route('/submit', methods = ['POST'])
def submit():
    data = {
        **request.form,
        "user_id" : session['user_id']
    }
    Submission.create_submission(data)
    return redirect('/dashboard')

@app.route('/verify/<division>/<g_ug>/<int:id>')
def verify_submissions_dynamic(division, g_ug, id):
    data = {
        "id" : id
    }
    Submission.verify_submission(data)
    return redirect(f"/verify/{division}/{g_ug}")

# @app.route('/verify/men/guided/<int:id>')
# def verify_mg(id):
#     data = {
#         "id" : id
#     }
#     Submission.verify_submission(data)
#     return redirect('/verify/mens/guided')

# @app.route('/verify/men/unguided/<int:id>')
# def verify_mu(id):
#     data = {
#         "id" : id
#     }
#     Submission.verify_submission(data)
#     return redirect('/verify/mens/unguided')

# @app.route('/verify/women/guided/<int:id>')
# def verify_wg(id):
#     data = {
#         "id" : id
#     }
#     Submission.verify_submission(data)
#     return redirect('/verify/womens/guided')

# @app.route('/verify/women/unguided/<int:id>')
# def verify_wu(id):
#     data = {
#         "id" : id
#     }
#     Submission.verify_submission(data)
#     return redirect('/verify/womens/unguided')

# @app.route('/verify/youth/guided/<int:id>')
# def verify_yg(id):
#     data = {
#         "id" : id
#     }
#     Submission.verify_submission(data)
#     return redirect('/verify/youths/guided')

# @app.route('/verify/youth/unguided/<int:id>')
# def verify_yu(id):
#     data = {
#         "id" : id
#     }
#     Submission.verify_submission(data)
#     return redirect('/verify/youths/unguided')