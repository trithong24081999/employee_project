print("✅ consumer_1.py has started")

import pika
import json
import os
import django
import time
import sys

sys.path.insert(0, os.path.abspath("/app/backend"))  # 👈 make /app the import root
print(os.environ)
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'employee_project.settings')

django.setup()
print("🧠 DJANGO_SETTINGS_MODULE =", os.environ.get("DJANGO_SETTINGS_MODULE"))

from employees.models.employee import Employee  # ✅ use absolute import

def callback(ch, method, properties, body):
    print("🟢 Received message")
    data = json.loads(body)
    print(data)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def wait_for_rabbitmq(max_retries=10, delay=3):
    for i in range(max_retries):
        try:
            print(f"🔌 Trying to connect to RabbitMQ... (attempt {i+1})")
            credential = pika.PlainCredentials(username="thong", password="1")
            connection = pika.BlockingConnection(
                parameters=pika.ConnectionParameters(
                    host='rabbitmq',
                    port=5672,
                    virtual_host="my_host",
                    credentials=credential
                                                                                      ))
            print("✅ Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("❌ RabbitMQ not ready yet. Retrying...")
            time.sleep(delay)
    raise Exception("🚨 Failed to connect to RabbitMQ after multiple attempts")

def start_consuming():
    connection = wait_for_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    print("🟢 Waiting for messages...")
    channel.start_consuming()


if __name__ == '__main__':
    start_consuming()
