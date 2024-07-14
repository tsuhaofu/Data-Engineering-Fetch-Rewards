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
## Sample Ouput
Here is a sample output of the `SELECT * FROM user_logins;` query after running the ETL process:

```sql
               user_id                | device_type |                            masked_ip                             |                         masked_device_id                         | locale | app_version | create_date 
--------------------------------------+-------------+------------------------------------------------------------------+------------------------------------------------------------------+--------+-------------+-------------
 424cdd21-063a-43a7-b91b-7ca1a833afae | android     | a6d0e2f27f6111e10b06790db42f34123e724aa0fd24b280f4a0ef5ee986784c | 4f00c1a807b673887c7af517d0df68e6b41aecf8cbec26c71fe4c580664669ed | RU     | 2.3.0       | 2024-07-14
 c0173198-76a8-4e67-bfc2-74eaa3bbff57 | ios         | 7b03f7d723535706b4777384fc906d18a4376bb84cebb50dc22c6eb9bddf00cb | a857e702f98990716938a0d74c3dc2dc565e4448833e2cf91c6ab26fc0e9971f | PH     | 0.2.6       | 2024-07-14
 66e0635b-ce36-4ec7-aa9e-8a8fca9b83d4 | ios         | fa7fca28c658d75a751b60e262602e1b11f4149274af6ec0d8c82a8619a51437 | e84fb3e15175d0a2492de6c02a99595c1343db7321ad6bb5f62052edd00a84f8 |        | 2.2.1       | 2024-07-14
 181452ad-20c3-4e93-86ad-1934c9248903 | android     | b21d1c922d9e9d1b913ade3265baa7fc43c757976dcd7cac3ed2043176655396 | 94b571f680b8f41547047f24e385334265773d33ab643bfc6f1684e21b8b34d9 | ID     | 0.96        | 2024-07-14
 60b9441c-e39d-406f-bba0-c7ff0e0ee07f | android     | 587f5a111a1f2adb462f778574a91b93de3b29889deca6e25dd363588a5e0ccb | 3102ec6d1310b3db007305eaa5802b3831d4b4ae5f165e21ee1e3298f55e5616 | FR     | 0.4.6       | 2024-07-14
 5082b1ae-6523-4e3b-a1d8-9750b4407ee8 | android     | 8ff1dcf25f4b6b831000c6af50fe0ca5c03b8db525d3c8b955531d20e5904457 | 8d99f03f520c4faaf8cc1b0c2fcb88f9ece87e7984ca36bdb7feb98d53ba023d |        | 3.7         | 2024-07-14
 5bc74293-3ca1-4f34-bb89-523887d0cc2f | ios         | 4535674cdeafe9e1bbc4792de6891ddf6a6c21c7accd8087036402aefc7dc31e | facaa527add19a6ad0a9d3bc806b80e6e8b9cb2fcdedf4122ddc352035022832 | PT     | 2.2.8       | 2024-07-14
 92d8ceec-2e12-49f3-81bd-518fe66971ec | android     | befc41fae56d97b40286a8ca77c179ae8e513388c74a73608c234463a1cb7d5c | 19ca7209461ccf164747bc93d56efb2f16fc3f14b1e3cf404dc157746adb7063 | BR     | 0.5.5       | 2024-07-14
 05e153b1-4fa1-474c-bd7e-9f74d1c495e7 | android     | 0d7f5fae97d2b525c78ce18b97fc4eb814e54c3874917aaaefc5ee15802c457e | bd1bcce6493944b297b2e9d87163d7aa01856c8f23f1a660152e5c8ed54d85eb |        | 0.5.0       | 2024-07-14
 325c0f3d-da25-45ff-aff4-81816db069bc | android     | 5f1bb1f8901076482ca745b88ef02071bcf0abc887eabdb1d1a6c8b47dcdd841 | 16efd8b6baabc95d04083e6d573aa6aa95a0dba3f4ee594d1ed3f60ddd909b19 | RU     | 0.60        | 2024-07-14
```

## Thought Process

1. **Reading Messages**: Utilized boto3 to read messages from a local SQS queue.
2. **Masking PII**: Applied SHA256 hashing to mask device_id and ip fields, ensuring that duplicates can be identified while maintaining data security.
3. **Writing to Postgres**: Connected to a local Postgres database using psycopg2 and inserted the transformed data.

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
