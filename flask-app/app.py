from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap

# Database
import psycopg2 as psql
from psycopg2 import sql


app = Flask(__name__)
Bootstrap(app)


login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, email):
        self.email = email


@login_manager.user_loader
def user_loader(email):
    user = User(email)
    user.id = email

    return user


# Database Configuration
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "test"


# Connect to the database
try:
    conn = psql.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host="psql-app",
                        port="5432")
    cur = conn.cursor()
except:
    # Should do something here!
    pass

# Define models for categories, nominees, votes, and users here

userInfo = {
    "firstname" : "Maxwell",
    "lastname" :  "Agyemang"
}


@app.route("/", methods=['GET', 'POST'])
def index():
    # Display the list of categories and their nominees
    #categories = Category.query.all()
    #if current_user.authenticated:
        #return redirect(url_for('something'))
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():

    return render_template('register.html', titleAux="Register", userInfo=userInfo)

@app.route('/category_management', methods=['GET', 'POST'])
def category():
    topInfo = {"selectedProject": 2}
    categoryList = [
        {"id": 1, "name": "Category A"},
        {"id": 2, "name": "Category B"},
        {"id": 3, "name": "Category C"},
        {"id": 4, "name": "Category D"}
    ] 
    return render_template('category.html', titleAux="Category",userInfo=userInfo,topInfo=topInfo,categoryList=categoryList)

@app.route('/nominee_management', methods=['GET', 'POST'])
def nominees():
    nomineeInfo = [    {        "id" : 1,       "name" : "Atoo",     "category" : "Best Lecturer",    "age": 23,  "Votes": 45,        "department": "Computer Science"    }, 
                      {        "id" : 2,         "name" : "Barnes",   "category" : "Best Researcher",  "age": 22,  "Votes": 72,        "department": "Physics"    },  
                          {        "id" : 3,      "name" : "Choi",    "category" : "Best Professor",   "age": 21,  "Votes": 63,        "department": "Chemistry"    }]

    return render_template('nominee_managment.html', titleAux="Nominee Management",userInfo=userInfo,nomineeInfo=nomineeInfo)

@app.route('/admin_tracking', methods=['GET', 'POST'])
def admin():
    return render_template('admin.html', titleAux="Admin Tracking",userInfo=userInfo)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html', titleAux="Profile",userInfo=userInfo)


'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle user authentication and login
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check if email and password match a user in the database
        # If they do, create a user session and redirect to the index page
        # If they don't, display an error message and prompt the user to try again
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    # Handle user logout by ending the user session and redirecting to the login page
    # You can use Flask-Login to handle user sessions

    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Handle user registration
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # Check if email is already registered
        # If it is, display an error message and prompt the user to try again
        # If it isn't, create a new user in the database and redirect to the login page
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return render_template('register.html')
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))
    else: 
    '''
   # return render_template('register.html')

'''
@app.route('/vote/<int:category_id>', methods=['GET', 'POST'])
def vote(category_id):
    # Handle the voting process
    if request.method == 'POST':
        nominee_id = request.form['nominee_id']
        # Check if the user has already voted for this category
        # If they have, display an error message and prompt the user to try again
        # If they haven't, record their vote in the database and redirect to the index page
    else:
        category = Category.query.get(category_id)
        nominees = Nominee.query.filter_by(category_id=category_id).all()
        return render_template('vote.html', category=category, nominees=nominees)
'''

#@app.route('/category_management')
#def category_management():
    #return render_template('category.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
