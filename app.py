from flask import Flask, render_template, redirect, session, flash
from db_layer import db, connect_db
from models import User, Feedback
from forms import NewUserForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"


connect_db(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_db'

@app.route('/')
def show_home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if 'username' in session:
        flash("You are already logged in", 'danger')
        return redirect('/')

    form = NewUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()

        session["username"] = user.username
        flash('You have successfully registered', 'success')
        return redirect(f'/users/{username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if 'username' in session:
        flash("You are already logged in", 'danger')
        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        if User.authenticate(username, password):
            session["username"] = username
            flash('You have successfully logged in', 'success')
            return redirect(f'/users/{username}')

        flash('Incorrect username or password', 'danger')

    return render_template('login.html', form=form)

@app.route('/secret')
def show_secret():
    return "You made it!"

@app.route('/logout')
def logout_user():
    session.pop('username')
    return redirect('/')

@app.route('/users/<username>')
def show_user(username):
    if 'username' not in session:
        flash("You are not logged in", 'danger')
        return redirect('/')

    if session['username'] == username:
        user = User.query.get_or_404(username)
        return render_template('user.html', user=user)

    flash("You are not authorized to view this page", 'danger')
    return redirect('/')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'username' not in session:
        flash("You are not logged in", 'danger')
        return redirect('/')
    
    if session['username'] == username:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        flash("User deleted", 'success')
        return redirect('/')

    flash("You are not authorized to delete this user", 'danger')
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    if 'username' not in session:
        flash("You are not logged in", 'danger')
        return redirect('/')

    if session['username'] == username:
        form = NewFeedbackForm()

        user = User.query.get_or_404(username)

        if form.validate_on_submit():
            title = form.title.data
            text = form.text.data
            feedback = Feedback(title=title, text=text, username = user.username)
            db.session.add(feedback)
            db.session.commit()

            flash('You have successfully added new feedback', 'success')
            return redirect(f'/users/{username}')
        
        return render_template('add_feedback.html', form=form)

    flash("You are not authorized to add feedback for this user", 'danger')
    return redirect('/')

@app.route('/feedback/<int:id>/update', methods=['GET','POST'])
def edit_feedback(id):
    if 'username' not in session:
        flash("You are not logged in", 'danger')
        return redirect('/')

    feedback = Feedback.query.get_or_404(id)

    username = feedback.user.username

    if session['username'] == username:
        form = FeedbackForm(obj=feedback)

        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.text = form.text.data
            db.session.commit()

            flash('Feedback edited', 'success')
            return redirect(f'/users/{username}')
        
        return render_template('edit_feedback.html', form=form)

    flash("You are not authorized to add feedback for this user", 'danger')
    return redirect('/')

@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    if 'username' not in session:
        flash("You are not logged in", 'danger')
        return redirect('/')

    feedback = Feedback.query.get_or_404(id)

    username = feedback.user.username

    if session['username'] == username:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback deleted', 'success')
        return redirect(f'/users/{username}')
        
    flash("You are not authorized to delete this feedback", 'danger')
    return redirect('/')
   
   