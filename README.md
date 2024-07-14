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
