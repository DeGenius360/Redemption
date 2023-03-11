FROM python:3.10

WORKDIR /app
COPY app.py .
COPY . .
COPY templates templates/

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
RUN pip3 install flask gunicorn psycopg2-binary PyGithub Flask-WTF Flask-Bootstrap4 flask-login  bcrypt Flask-SQLAlchemy flask-socketio
CMD ["gunicorn", "--chdir", "/app", "app:app", "-b", "0.0.0.0:5000"]
