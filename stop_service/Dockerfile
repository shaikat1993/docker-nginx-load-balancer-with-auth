FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    && curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose \
    && apt-get install -y docker.io \
    && apt-get clean

# Install Python dependencies
RUN pip install flask

# Set the working directory
WORKDIR /app

# Copy the stop service code
COPY . /app/stop_service/

# Make sure the script is executable
RUN chmod +x /app/stop_service/stop_containers.sh

# Expose the necessary port
EXPOSE 8210

CMD ["python", "/app/stop_service/stop_service.py"]
