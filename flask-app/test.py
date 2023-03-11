from flask import Flask, current_app
from .test import bp as test_bp

app = Flask(__name__)
app.register_blueprint(test_bp)

# define database connection here...

@app.teardown_appcontext
def close_db_connection(error):
    """Close database connection at end of request"""
    conn = current_app.db
    if conn is not None:
        conn.commit()
        conn.close()