# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY ./requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy the entire directory files
COPY . . 

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
