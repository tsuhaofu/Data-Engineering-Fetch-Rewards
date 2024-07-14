# Data-Engineering-Fetch-Rewards

## Overview

This project demonstrates the ability to build and maintain real-time data pipelines that process data from an AWS SQS Queue, mask personally identifiable information (PII), and write the transformed data to a Postgres database. The environment is set up using Docker to run all components locally, including the SQS Queue and Postgres database. This project aligns with the role of a Data Engineer at Fetch Rewards, which involves developing event-based real-time data pipelines and ensuring data integrity and security.

## System Information

### Host System

- **Operating System**: macOS Sonoma 14.5
- **Docker**: 20.10.17
- **Docker Compose**: 2.10.2
- **AWS CLI Local**: 1.33.26
- **PostgreSQL Client**: 14.12
- **Python**: 3.10.9

### Docker Container System

- **Base Image**: `python:3.9-slim`
- **Operating System**: Debian-based slim variant
- **Python Version**: 3.9

## Setup and Running the Application

### Prerequisites

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/tsuhaofu/Data-Engineering-Fetch-Rewards.git
   cd fetch_rewards_etl
   ```

2. **Install Required Tools:**

Docker: Installation Guide
Docker Compose: Included with Docker Desktop
AWS CLI Local: pip install awscli-local
PostgreSQL Client: Installation Guide

3. **Install Python Dependencies:**

```sh
pip install -r requirements.txt
```

### Project Setup

1. **Start Docker Containers:**

```sh
docker-compose up -d
```

2. **Build and Run ETL Application:**

```sh
docker build -t fetch_etl
docker run --network="host" fetch_etl
```

###Verifying the Setup

1.**Read a Message from the Queue:**

``sh
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
``

Connect to the Postgres Database:

sh
Copy code
psql -d postgres -U postgres -p 5432 -h localhost -W
Verify the Table and Data:

sql
Copy code
SELECT * FROM user_logins;
Database Schema
The target table user_logins is created with the following DDL:

sql
Copy code
CREATE TABLE IF NOT EXISTS user_logins(
    user_id             varchar(128),
    device_type         varchar(32),
    masked_ip           varchar(256),
    masked_device_id    varchar(256),
    locale              varchar(32),
    app_version         varchar(32),
    create_date         date
);
Thought Process
Reading Messages: Utilized boto3 to read messages from a local SQS queue.
Masking PII: Applied SHA256 hashing to mask device_id and ip fields, ensuring that duplicates can be identified while maintaining data security.
Writing to Postgres: Connected to a local Postgres database using psycopg2 and inserted the transformed data.
Docker: Employed Docker to containerize the application for consistency, portability, and ease of deployment.
Detailed Implementation
Docker Compose File
yaml
Copy code
version: "3.9"
services:
  localstack:
    image: fetchdocker/data-takehome-localstack
    ports:
      - "4566:4566"

  postgres:
    image: fetchdocker/data-takehome-postgres
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_USER: postgres
    ports:
      - "5432:5432"
ETL Script (src/main.py)
python
Copy code
import os
import hashlib
import boto3
import psycopg2
from datetime import datetime
import json

# Set dummy AWS credentials for localstack
os.environ['AWS_ACCESS_KEY_ID'] = 'dummy'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'dummy'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

def mask_pii(value):
    return hashlib.sha256(value.encode()).hexdigest()

def receive_messages():
    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1')
    response = sqs.receive_message(
        QueueUrl='http://localhost:4566/000000000000/login-queue',
        MaxNumberOfMessages=10,
    )
    return response.get('Messages', [])

def process_message(message):
    body = json.loads(message['Body'])
    transformed_data = {
        'user_id': body['user_id'],
        'device_type': body['device_type'],
        'masked_ip': mask_pii(body['ip']),
        'masked_device_id': mask_pii(body['device_id']),
        'locale': body['locale'],
        'app_version': str(body['app_version']),  # Ensure app_version is a string
        'create_date': datetime.now()
    }
    return transformed_data

def write_to_postgres(data):
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, (
        data['user_id'], data['device_type'], data['masked_ip'], data['masked_device_id'], data['locale'], data['app_version'], data['create_date']
    ))
    conn.commit()
    cursor.close()
    conn.close()

def main():
    messages = receive_messages()
    for message in messages:
        transformed_data = process_message(message)
        write_to_postgres(transformed_data)

if __name__ == "__main__":
    main()
Dockerfile
Dockerfile
Copy code
FROM python:3.9-slim

WORKDIR /app

COPY src/main.py .

RUN pip install boto3 psycopg2-binary

# Set dummy AWS credentials
ENV AWS_ACCESS_KEY_ID=dummy
ENV AWS_SECRET_ACCESS_KEY=dummy
ENV AWS_DEFAULT_REGION=us-east-1

CMD ["python", "main.py"]
requirements.txt
makefile
Copy code
boto3==1.18.69
psycopg2-binary==2.9.1
Questions and Answers
How would you deploy this application in production?
I would deploy this application using a managed Kubernetes service like AWS EKS or GCP GKE. Kubernetes provides scalability, reliability, and automated management of containerized applications. The components would be deployed as microservices, allowing independent scaling and maintenance.

What other components would you want to add to make this production ready?
To make this application production-ready, I would add:

Monitoring and Logging: Implement tools like Prometheus for monitoring and the ELK stack (Elasticsearch, Logstash, Kibana) for centralized logging.
CI/CD Pipeline: Set up continuous integration and continuous deployment (CI/CD) pipelines using Jenkins or GitHub Actions to automate testing and deployment processes.
Secrets Management: Use AWS Secrets Manager or HashiCorp Vault to securely manage sensitive information.
Error Handling and Alerts: Incorporate comprehensive error handling and set up alerting mechanisms to notify of any issues in real-time.
How can this application scale with a growing dataset?
This application can scale with a growing dataset by:

Horizontal Scaling: Adding more instances of the ETL service to handle increased load.
Distributed Messaging: Using a distributed messaging system like Apache Kafka instead of SQS for better scalability and fault tolerance.
Database Sharding: Implementing sharding in the Postgres database to distribute the load across multiple database instances.
How can PII be recovered later on?
PII can be recovered later on by storing the mapping of original values to their hashed values in a secure, separate database. This allows for the recovery of original PII if necessary while maintaining data security.

What are the assumptions you made?
The structure of the JSON messages remains consistent.
The SQS queue and Postgres database are properly configured and accessible.
The device_id and ip fields are to be masked using SHA256 hashing to ensure duplicates can be identified.
Scope of Responsibilities
This project aligns with the role of a Data Engineer at Fetch Rewards by demonstrating the ability to:

Develop event-based real-time data pipelines that filter, join, sort, and manipulate data into useful aggregations.
Write efficient and scalable code in Python.
Understand and handle the complexities of distributed systems, ensuring resilience to failures.
Identify and fix performance bottlenecks in high throughput pipelines.
Communicate effectively, translating and explaining technical issues to non-technical team members.
