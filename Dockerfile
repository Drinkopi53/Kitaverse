# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Panda3D system dependencies
RUN apt-get update && apt-get install -y \\
    libgl1 \\
    libglu1 \\
    libxmu6 \\
    libxi6 \\
    libxrandr2 \\
    libxcursor1 \\
    libxinerama1 \\
    libxft2 \\
    libfreetype6 \\
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Run the server
CMD ["python", "app/backend/main.py"]