# Use an official Python image as the base
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expose the port that the Django development server will use
EXPOSE 8000

# Run the command to start the Django development server when the container starts
CMD ["gunicorn", "shop.wsgi:application", "--bind", "0.0.0.0:8000"]
