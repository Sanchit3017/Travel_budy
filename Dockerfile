FROM --platform=linux/arm64 public.ecr.aws/amazonlinux/amazonlinux:2023-arm64


# Install Python
RUN dnf install -y python3 python3-pip git

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
