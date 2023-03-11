from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, current_app, session
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
import bcrypt
import os
os.urandom(16)

# Database
import psycopg2 as psql
from psycopg2 import sql


app = Flask(__name__)
app.secret_key = 'my-secret-key'
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
    #get the message from the session if it exists
    message = session.pop('message', None)
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    return render_template("index.html",userInfo=userInfo, message=message)

@app.route('/loginresponse', methods=['GET','POST'])
def loginresponse():
    try:
        email = request.form.get('login_email')
        password = request.form.get('login_password')
        if email == None or password is None:
            flash('No email and password provided')
            return redirect(url_for('index'))
        
        # check if we have correct login credentials
        query = '''
            SELECT 1 FROM users WHERE email = %s and password=crypt(%s, salt)
        '''
        cur.execute(query, [email,password])
        result = cur.fetchall()
        print('user:', result)
        if result != []:
            user_obj = User(email)
            user_obj.id = email
            login_user(user_obj, remember=False)
            print('User logged in successfully')
            flash('Login successful', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Incorrect email or password', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        print('You fucker!')
        flash(f'Failed to login: {e}')
        return redirect(url_for('index'))
    
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("index"))
       

    

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    #check if it's a post request
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_repeat = request.form.get('password_repeat')

        #make sure password and confirm password match
        if password != password_repeat:
            flash('Passwords do not match')
            return redirect(url_for('index'))

        #check if the user is already present in the database 
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users where email=%s", (email,))
        user = cur.fetchone()

        if user:
                flash('This email is already registered.')
                return redirect(url_for('register'))
        

        #add the new user to the database
        registerQuery = sql.SQL(
        """INSERT INTO users (name,email, password, salt) VALUES(%s, %s, %s, gen_salt('bf', 8))""")
        cur.execute(registerQuery, (f'{first_name} {last_name}', email, password))
        conn.commit()

        #hash the password
         # Hash the password
        hashQuery = sql.SQL(
            """UPDATE users SET password=crypt(password, salt) WHERE email=%s""")
        cur.execute(hashQuery, [email])
        conn.commit()

        flash('You have successfully registered.')
        session['message'] = 'You have successfully registered'
        return redirect(url_for('loginresponse')) 
        
   
    return render_template('register.html', titleAux="Register", userInfo=userInfo)

@app.route('/category_management', methods=['GET', 'POST'])
@login_required
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
@login_required
def nominees():
    nomineeInfo = [    {        "id" : 1,       "name" : "Atoo",     "category" : "Best Lecturer",    "age": 23,  "Votes": 45,        "department": "Computer Science"    }, 
                      {        "id" : 2,         "name" : "Barnes",   "category" : "Best Researcher",  "age": 22,  "Votes": 72,        "department": "Physics"    },  
                          {        "id" : 3,      "name" : "Choi",    "category" : "Best Professor",   "age": 21,  "Votes": 63,        "department": "Chemistry"    }]

    return render_template('nominee_managment.html', titleAux="Nominee Management",userInfo=userInfo,nomineeInfo=nomineeInfo)

@app.route('/admin_tracking', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin.html', titleAux="Admin Tracking",userInfo=userInfo)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', titleAux="Profile",userInfo=userInfo)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
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



