FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (relative to build context root)
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# FORCE STABLE VERSIONS for Cloud (Overrides requirements.txt if needed)
# This ensures stability on Hugging Face even if local requirements are different
RUN pip install --no-cache-dir mediapipe==0.10.9 protobuf==3.20.3

# Copy backend and model directories (relative to build context root)
COPY backend/ /app/backend/
COPY model/ /app/model/

# Set working directory to backend
WORKDIR /app/backend

# Expose the port that Hugging Face Spaces expects (7860)
EXPOSE 7860

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
