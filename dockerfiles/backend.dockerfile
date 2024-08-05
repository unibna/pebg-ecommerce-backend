# Use the official Python base image
FROM python:3.11.8-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY src/requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the Django project to the container
COPY src/ .

# Expose the port that Django runs on
EXPOSE 8000

# Set the command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
