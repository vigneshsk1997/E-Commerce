# Use an official Python runtime as the base image
FROM python:3.10-slim

# Install system dependencies for PostgreSQL and other utilities
RUN apt-get update && \
    apt-get install -y libpq-dev gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app/

# Download the wait-for-it.sh script to manage database readiness
RUN curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x wait-for-it.sh

# Install the Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8081 for the application to communicate on
EXPOSE 8081

# Set the command to run the wait-for-it script and then the Django development server
CMD ["./wait-for-it.sh", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8081"]
