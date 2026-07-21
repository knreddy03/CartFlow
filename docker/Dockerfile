# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN pip install --no-cache-dir uv

RUN uv sync --frozen 

# Copy the full project into /app
COPY . .

# Expose app port
EXPOSE 8000

# Default command to start app
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]