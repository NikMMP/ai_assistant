# Use the official Python 3.9 image as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc libmagic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install the project dependencies
RUN poetry config virtualenvs.create false && \
    poetry install

# Copy the rest of the application code
COPY . /app/

# Default command to start the application
CMD poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
