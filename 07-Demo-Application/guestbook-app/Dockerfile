# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the src directory to the working directory
COPY ./src /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run main.py when the container launches using gunicorn as a production server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]