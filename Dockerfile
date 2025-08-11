FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app_1.py /app/app.py

# Install dependencies
RUN pip install flask psycopg2-binary

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
