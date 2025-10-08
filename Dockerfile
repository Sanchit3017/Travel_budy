# Use the official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install dependencies (if requirements.txt exists)


# Run your Python file
CMD ["python", "travel_intake_agent.py"]
