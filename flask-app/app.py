from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# Database
import psycopg2 as psql
from psycopg2 import sql


app = Flask(__name__)



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




@app.route('/')
def index():
    # Display the list of categories and their nominees
    categories = Category.query.all()
    return render_template('index.html', categories=categories)


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
    else:
        return render_template('register.html')


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


if __name__ == '__main__':
    app.run(debug=True)
