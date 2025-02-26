# Use a base image that matches your application's environment
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install any system dependencies (if necessary)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code to the container
COPY . /app

# Install the Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 8080

# Set environment variables for Flask to run on the right host
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PORT=8080

# Command to run the Flask app with gunicorn for production
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080"]
