# Dockerfile

# Use the official Python image with slim version
FROM python:3.12.3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to a temporary location
COPY requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port on which the Flask app will run
ENV PORT 5000
EXPOSE $PORT

# Load environment variables from .env file
ENV PATH_TO_ENV /app/.env
RUN if [ -f "$PATH_TO_ENV" ]; then export $(cat $PATH_TO_ENV | grep -v '^#' | xargs); fi

# Set the default Flask app
CMD ["gunicorn", "hbnb:app", "-w", "2", "-b", "0.0.0.0:$PORT"]

