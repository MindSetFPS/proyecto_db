# Use an official Python image as the base
FROM python:3.12-slim

RUN apt update -y
RUN apt install libpq-dev postgresql postgresql-contrib -y

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

RUN chmod +x ./docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "./docker-entrypoint.sh" ]