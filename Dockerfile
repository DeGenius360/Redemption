FROM python:3.8

# Add PostgreSQL binaries to PATH
ENV PATH "$PATH:/usr/lib/postgresql/{version}/bin"

# Install dependencies
RUN apt-get update && apt-get install -y \
    postgresql \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

# Create and set the working directory
WORKDIR /app

# Copy the dependencies file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY flask-app /app

# Copy the schema file
COPY psql-app/schema.sql /docker-entrypoint-initdb.d/

# Create a volume for the postgres data
VOLUME ["/var/lib/postgresql/data"]

# Expose port 5000
EXPOSE 5000

# Start PostgreSQL and run schema.sql
CMD ["pg_ctl", "start", "-D", "/var/lib/postgresql/data/", "&&", "psql", "-U", "postgres", "-f", "/docker-entrypoint-initdb.d/schema.sql", "&&", "pg_ctl", "stop", "-D", "/var/lib/postgresql/data/"]

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
