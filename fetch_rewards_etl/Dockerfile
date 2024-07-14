FROM python:3.9-slim

WORKDIR /app

COPY src/main.py .

RUN pip install boto3 psycopg2-binary

# Set dummy AWS credentials
ENV AWS_ACCESS_KEY_ID=dummy
ENV AWS_SECRET_ACCESS_KEY=dummy
ENV AWS_DEFAULT_REGION=us-east-1

CMD ["python", "main.py"]

