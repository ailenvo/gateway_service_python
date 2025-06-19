# Dockerfile
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --progress-bar off --no-cache-dir -r requirements.txt 

# Copy the application code
COPY . .

# Expose the port on which FastAPI will run
EXPOSE 8000

# Run the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
