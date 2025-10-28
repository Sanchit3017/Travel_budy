
FROM public.ecr.aws/amazonlinux/amazonlinux:2023

RUN dnf install -y python3 python3-pip git


WORKDIR /app


COPY . .


RUN pip install boto3 requests agentcore


CMD ["python3", "main.py"]

