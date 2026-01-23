# FROM python:3.11-slim 

# # Set working directory
# WORKDIR /app 

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# Use Python 3.11 slim image
#FROM python:3.11-slim

# Use official Microsoft Playwright Python image (guaranteed to work)
#FROM mcr.microsoft.com/playwright/python:v1.52.0-focal
FROM mcr.microsoft.com/playwright/python:v1.50.0-noble

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
#ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
# ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
# ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     g++ \
#     curl \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     g++ \
#     curl \
#     build-essential \
#     wget \
#     fonts-liberation \
#     libasound2 \
#     libatk-bridge2.0-0 \
#     libatk1.0-0 \
#     libatspi2.0-0 \
#     libc6 \
#     libcairo2 \
#     libcups2 \
#     libdbus-1-3 \
#     libexpat1 \
#     libgbm1 \
#     libgcc1 \
#     libglib2.0-0 \
#     libgtk-3-0 \
#     libnspr4 \
#     libnss3 \
#     libpango-1.0-0 \
#     libpangocairo-1.0-0 \
#     libstdc++6 \
#     libx11-6 \
#     libx11-xcb1 \
#     libxcb1 \
#     libxcomposite1 \
#     libxcursor1 \
#     libxdamage1 \
#     libxext6 \
#     libxfixes3 \
#     libxrandr2 \
#     libxrender1 \
#     libxss1 \
#     && rm -rf /var/lib/apt/lists/*


# Upgrade pip first
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install packages individually to avoid conflicts and speed up builds
# Core dependencies first
# RUN pip install --no-cache-dir protobuf==3.20.3
# RUN pip install --no-cache-dir python-dotenv==1.1.1
# RUN pip install --no-cache-dir beautifulsoup4==4.13.4

# Copy requirements first for beter caching
COPY requirements.txt .

# Install Python dependencies

RUN pip install --no-cache-dir -r requirements.txt 

#RUN playwright install --with-deps chromium

# FORCE MATCH
# RUN pip install --no-cache-dir playwright==1.50.0
# RUN python -m playwright install chromium
# RUN python -m playwright install --with-deps chromium

# Copy application code
# COPY . .

# # Create necessary directories
# RUN mkdir -p /app/data /app/chroma_db /app/.streamlit 

# # Copy Streamlit config 
# COPY .streamlit/config.toml /app/.streamlit/config.toml

# Playwright - install without browsers to save time and space
# RUN pip install --no-cache-dir playwright==1.52.0
RUN playwright install chromium --with-deps
#RUN playwright install-deps chromium
# # needed as docker container doesnt have gui support thus it needs playwright deps for docker 
# RUN playwright install-deps

COPY . .

RUN ls -la
# Debug: List Python files and check imports
RUN ls -la /app/
RUN python -c "import sys; print('Python path:', sys.path)"
RUN python -c "import os; print('Files in /app:', os.listdir('/app'))"

# Debug: Check if book_workflow.py exists and its contents
RUN if [ -f "book_workflow.py" ]; then echo "book_workflow.py exists"; else echo "book_workflow.py NOT FOUND"; fi
RUN if [ -f "book_workflow.py" ]; then head -20 book_workflow.py; fi


# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/temp

# Expose Streamlit port
EXPOSE 8080

# Health check
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#     CMD curl -f http://localhost:8080/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true", "--server.fileWatcherType=none", "--browser.gatherUsageStats=false"]
# CMD streamlit run main.py \
#     --server.port=$PORT \
#     --server.address=0.0.0.0 \
#     --server.headless=true \
#     --server.fileWatcherType=none \
#     --browser.gatherUsageStats=false