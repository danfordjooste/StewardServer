import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, render_template
from flask_migrate import Migrate

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URI',
    'postgresql://postgres:root@localhost/flasktut1')
    
#app.config['SECRET_KEY'] = 'super-secret'
#app.config['SECURITY_REGISTERABLE'] = True
#app.debug = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
            self.username = username
            self.email = email
    
    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index():
    myUser = User.query.all()
    oneItem = User.query.filter_by(username="test2").all()
    return render_template('add_user.html', myUser=myUser,oneItem=oneItem)

@app.route('/post_user', methods=['POST'])
def post_user():
    user = User(request.form['username'], request.form['email'])
    # this add to the database the user
    db.session.add(user)
    # this saves this data in the database
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()