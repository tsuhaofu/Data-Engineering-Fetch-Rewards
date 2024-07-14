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

- **Docker**: [Installation Guide](https://docs.docker.com/get-docker/)
- **Docker Compose**: Included with Docker Desktop
- **AWS CLI Local**: `pip install awscli-local`
- **PostgreSQL Client**: [Installation Guide](https://www.postgresql.org/download/)

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

### Verifying the Setup

1.**Read a Message from the Queue:**

```sh
as local sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
```

2. **Connect to the Postgres Database:**

```sh
psql -d postgres -U postgres -p 5432 -h localhost -W
```
3. **Verify the Table and Data:**

```sql
SELECT * FROM user_logins;
```

## Database Schema
The target table `user_logins` is created with the following DDL:

```sql
CREATE TABLE IF NOT EXISTS user_logins(
    user_id             varchar(128),
    device_type         varchar(32),
    masked_ip           varchar(256),
    masked_device_id    varchar(256),
    locale              varchar(32),
    app_version         varchar(32),
    create_date         date
);
```
## Thought Process

1. **Reading Messages**: Utilized boto3 to read messages from a local SQS queue.
2. **Masking PII**: Applied SHA256 hashing to mask device_id and ip fields, ensuring that duplicates can be identified while maintaining data security.
3. **Writing to Postgres**: Connected to a local Postgres database using psycopg2 and inserted the transformed data.

requirements.txt
makefile
Copy code
boto3==1.18.69
psycopg2-binary==2.9.1

## Questions and Answers

### How would you deploy this application in production?
I would deploy this application using a managed Kubernetes service like AWS EKS or GCP GKE. Kubernetes provides scalability, reliability, and automated management of containerized applications. The components would be deployed as microservices, allowing independent scaling and maintenance.

### What other components would you want to add to make this production ready?
To make this application production-ready, I would add:

- **Monitoring and Logging**: Implement tools like Prometheus for monitoring and the ELK stack (Elasticsearch, Logstash, Kibana) for centralized logging.
- **CI/CD Pipeline**: Set up continuous integration and continuous deployment (CI/CD) pipelines using Jenkins or GitHub Actions to automate testing and deployment processes.
- **Secrets Management**: Use AWS Secrets Manager or HashiCorp Vault to securely manage sensitive information.
- **Error Handling and Alerts**: Incorporate comprehensive error handling and set up alerting mechanisms to notify of any issues in real-time.
  
### How can this application scale with a growing dataset?
This application can scale with a growing dataset by:

- **Horizontal Scaling**: Adding more instances of the ETL service to handle increased load.
- **Distributed Messaging**: Using a distributed messaging system like Apache Kafka instead of SQS for better scalability and fault tolerance.
- **Database Sharding**: Implementing sharding in the Postgres database to distribute the load across multiple database instances.

### How can PII be recovered later on?
PII can be recovered later on by storing the mapping of original values to their hashed values in a secure, separate database. This allows for the recovery of original PII if necessary while maintaining data security.

### What are the assumptions you made?
- The structure of the JSON messages remains consistent.
- The SQS queue and Postgres database are properly configured and accessible.
- The device_id and ip fields are to be masked using SHA256 hashing to ensure duplicates can be identified.
  
### Scope of Responsibilities
This project aligns with the role of a Data Engineer at Fetch Rewards by demonstrating the ability to:

- Develop event-based real-time data pipelines that filter, join, sort, and manipulate data into useful aggregations.
- Write efficient and scalable code in Python.
- Understand and handle the complexities of distributed systems, ensuring resilience to failures.
- Identify and fix performance bottlenecks in high throughput pipelines.
- Communicate effectively, translating and explaining technical issues to non-technical team members.
