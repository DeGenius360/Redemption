FROM python:3.10

WORKDIR /app
COPY app.py .
COPY templates templates/
RUN pip3 install flask gunicorn psycopg2-binary PyGithub Flask-WTF Flask-Bootstrap4 flask-login Flask-SQLAlchemy
CMD ["gunicorn", "--chdir", "/app", "app:app", "-b", "0.0.0.0:5000"]
