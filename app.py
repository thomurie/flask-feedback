from flask import Flask, request, jsonify, render_template, redirect, session, flash

from models import User, db, connect_db, Feedback

from forms import NewUserForm, LoginUserForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456789'

connect_db(app)
db.create_all()


@app.route('/', methods = ['GET'])
def home():
    return redirect('/register')

@app.route('/register', methods = ['GET', 'POST'])
def show_user_registration_form():
    form = NewUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username = username, password = password, email = email, first_name = first_name, last_name = last_name)
        db.session.commit()

        session['user_id'] = new_user.username
        return redirect(f'/user/{new_user.username}')

    else:
        return render_template('index.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login_user_form():

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if User.query.filter_by(username = username) == False:
            return redirect('/')
        if  User.authenticate(username, password): 
            user = User.authenticate(username, password)
            session['user_id'] = user.username
            return redirect(f'/user/{user.username}')
        else: 
            session['user_id'] = None
            flash('Incorrect Username or Password')
            return render_template('login_form.html', form = form)
    else:
        return render_template('login_form.html', form = form)

@app.route('/user/<username>', methods = ['GET'])
def accessing_secret(username):
    if username != session["user_id"]:
        return redirect('/')
    if session['user_id']:
        flash(f'Welcome {username}')
        user = User.query.filter_by(username = session['user_id']).first()
        user_feedback = Feedback.query.filter_by(username = session['user_id']).all()
        return render_template('secret.html', user = user, feedbacks = user_feedback)
    else:
        return redirect('/login')

@app.route('/logout', methods = ['GET'])
def logout_user():
    session['user_id'] = None
    return redirect('/')

@app.route('/user/<username>/delete', methods = ['POST'])
def remove_user(username):
    if session['user_id'] == username:
        if Feedback.query.filter_by(username = username).all():
            feedbacks = Feedback.query.filter_by(username = username).all()
            for feedback in feedbacks:
                db.session.delete(feedback)
        user = User.query.filter_by(username = session['user_id']).first()
        db.session.delete(user)
        db.session.commit()
        session['user_id'] = None
        return redirect('/')
    else: 
        session['user_id'] = None
        return redirect('/')

@app.route('/user/<username>/feedback/add', methods = ['GET','POST'])
def add_user_feedback(username):
    if session['user_id'] == username:
        form = FeedbackForm()
        user = User.query.filter_by(username = username).first()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_feedback = Feedback(title = title, content=content, username = username)
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f'/user/{username}')
        
        else:
            return render_template('add_feedback.html', form = form, user=user)

    else:
        return redirect('/logout')

@app.route('/feedback/<int:feedback_id>/update', methods = ['GET','POST'])
def update_user_feedback(feedback_id):
    feedback = Feedback.query.filter_by(id = int(feedback_id)).first()
    form = FeedbackForm()

    if session['user_id'] == feedback.username:
        form = FeedbackForm()
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(f'/user/{feedback.username}')
        
        else:
            return render_template('update_feedback.html', feedback = feedback, form = form)

    else:
        return redirect('/logout')

@app.route('/feedback/<int:feedback_id>/delete', methods = ['POST'])
def remove_feedback(feedback_id):
    feedback = Feedback.query.filter_by(id = int(feedback_id)).first()
    if session['user_id'] == feedback.username:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/user/{feedback.username}')
    else:
        return redirect('/logout')