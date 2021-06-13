from app import app
from models import db, User, Feedback


db.drop_all()
db.create_all()

u1 = User.register(username = "john123", password = "123456789", email = 'user1@gmail.com', first_name="john1", last_name='123')

u2 = User.register(username = "john223", password = "123456789", email = 'user2@gmail.com', first_name="john2", last_name='123')

u3 = User.register(username = "john323", password = "123456789", email = 'user3@gmail.com', first_name="john3", last_name='123')

feedback1 = Feedback(title = 'title1', content = 'content1', username = 'thom')
feedback2 = Feedback(title = 'title2', content = 'content2', username = 'thom')
feedback3 = Feedback(title = 'title3', content = 'content3', username = 'thom')

db.session.add(feedback1)
db.session.add(feedback2)
db.session.add(feedback3)
db.session.commit()

