from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os  # For environment variables

app = Flask(__name__)

# Load secret key from an environment variable for better security
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'verysecretkey')  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # Still plaintext - bad practice!

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Vulnerable SQL Injection
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first() 
        if user:
            return redirect(url_for('home'))
        else:
            return 'Login Failed'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if request.method == 'POST':
        comment = Comment(content=request.form['content'], user_id=1) 
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('comment.html')

@app.route('/profile/<username>')
def profile(username):
    # XSS Vulnerability
    return render_template('profile.html', username=username) 

if __name__ == '__main__':
    app.run(debug=False)
