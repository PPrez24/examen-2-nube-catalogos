# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add build arguments for database credentials
ARG DB_HOST
ARG DB_USER
ARG DB_PASSWORD
ARG DB_NAME
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_SESSION_TOKEN

# Set environment variables inside container
ENV DB_HOST=$DB_HOST
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_NAME=$DB_NAME
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN

# Expose the port
EXPOSE 5000 

# Start the application
CMD ["python", "app.py"]
