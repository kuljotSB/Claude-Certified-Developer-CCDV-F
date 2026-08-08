# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file if you have one
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy MCP server code
COPY . .

# Expose port (change if your MCP server uses a different port)
EXPOSE 8000

# Set environment variables if needed
# ENV ENV_VAR_NAME=value

# Start MCP server (replace 'main.py' with your actual entrypoint)
CMD ["python", "server.py"]