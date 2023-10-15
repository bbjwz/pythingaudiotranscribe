# Use a Python base image
FROM python:3.8-slim-buster

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app will run on
EXPOSE 8000

# Use gunicorn to serve the application
CMD ["gunicorn", "transcription.wsgi:application", "--bind", "0.0.0.0:8000"]
