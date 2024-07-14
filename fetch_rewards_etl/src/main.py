import os
import hashlib
import boto3
import psycopg2
from datetime import datetime
import json

# Set dummy AWS credentials for localstack
#os.environ['AWS_ACCESS_KEY_ID'] = 'dummy'
#os.environ['AWS_SECRET_ACCESS_KEY'] = 'dummy'
#os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

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

