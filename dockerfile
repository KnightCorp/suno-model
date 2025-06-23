# Use official slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install OS packages
RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

# Copy code
COPY . .

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Preload Bark model (optional but speeds up first call)
RUN python -c "from bark import preload_models; preload_models()"

# Expose the port FastAPI uses
EXPOSE 8080

# Start FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
