# Use the official Python image as the base image
FROM python:3.9-slim

# Set a working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Ensure pip is updated
RUN pip install --upgrade pip

# Install required Python packages
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Command to run your application
CMD ["python", "main.py"]
