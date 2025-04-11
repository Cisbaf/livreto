# Use the official Python image from the Docker Hub
FROM python:3.12.9

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev pkg-config default-libmysqlclient-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy src
COPY /src .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
