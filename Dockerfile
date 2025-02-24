FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pytest pytest-env

# Copy project files
COPY . .

# Make scripts executable and fix permissions
COPY entrypoint.sh initialize_database.sh ./
RUN chmod +x entrypoint.sh initialize_database.sh \
    && chown -R root:root /app \
    && chmod -R 755 /app

# Set the entrypoint script
ENTRYPOINT ["sh", "./entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"] 