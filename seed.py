from models import User, Feedback
from app import app
from db_layer import db

db.drop_all()
db.create_all()


user1 = User.register(username='bob', password='password1', email='bob@gmail.com', first_name='bob', last_name='jones')
user2 = User.register(username='jane', password='password2', email='jane@gmail.com', first_name='jane', last_name='jones')
user3 = User.register(username='sam', password='password3', email='sam@gmail.com', first_name='sam', last_name='smith')

users = [user1, user2, user3]
db.session.add_all(users)
db.session.commit()

fb1 = Feedback(title="Great job", text="Keep up the good work", username='bob') 
fb2 = Feedback(title="Nevermind", text="You're doing such a bad job", username='bob') 
fb3 = Feedback(title="Fixed", text="Sorry, changed my mind", username='bob') 
fb4 = Feedback(title="Helpful", text="Very good service", username='jane') 

feedback = [fb1, fb2, fb3, fb4]
db.session.add_all(feedback)
db.session.commit()