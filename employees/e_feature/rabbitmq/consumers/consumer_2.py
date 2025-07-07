print("✅ consumer_2.py has started")

import pika
import json
import os
import django
import time
import sys
sys.path.insert(0, os.path.abspath("/app"))

os.environ.setdefault(key="DJANGO_SETTINGS_MODULE",
                      value='employee_project.settings')
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
            credentials = pika.PlainCredentials(username='user_a', password='1')
            print(f"🔌 Trying to connect to RabbitMQ... (attempt {i+1})")
            connection = pika.BlockingConnection(parameters=
                                                 pika.ConnectionParameters(
                                                     host='rabbitmq', port=5672,
                                                     virtual_host="host_a",
                                                     credentials=credentials))
            print("✅ Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("❌ RabbitMQ not ready yet. Retrying...")
            time.sleep(delay)
    raise Exception("🚨 Failed to connect to RabbitMQ after multiple attempts")

def start_consuming():
    connection = wait_for_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='odoo_queue', durable=True)
    channel.queue_bind(queue='odoo_queue', exchange='message_router', routing_key='odoo_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='odoo_queue', on_message_callback=callback)
    print("🟢 Waiting for messages...")
    channel.start_consuming()


if __name__ == '__main__':
    start_consuming()
