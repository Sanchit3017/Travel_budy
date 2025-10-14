FROM --platform=linux/arm64 python:3.9-alpine


# Install Python



# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Install dependencies
RUN pip install boto3 requests

# Expose port
EXPOSE 8080

# Command to start agentcore runtime
CMD ["python3", "main.py"]
