import pika
import uuid

# RabbitMQ connection parameters
rabbitmq_host = '13.233.39.76'  # Change to the appropriate hostname or IP address if needed
rabbitmq_port = 5672
rabbitmq_user = 'guest'
rabbitmq_password = 'guest'
exchange_name = '/event/1/user1@videonetics.com'

# Generate a unique queue name for this consumer instance
queue_name = f'{exchange_name}_{str(uuid.uuid4())[:8]}'  # Unique queue name

# Establish a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password)))
channel = connection.channel()

# Declare the fanout exchange
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

# Declare a queue for this consumer
channel.queue_declare(queue=queue_name)

# Bind the queue to the fanout exchange
channel.queue_bind(exchange=exchange_name, queue=queue_name)

print(f" [*] Waiting for broadcast messages. To exit, press Ctrl+C")

# Callback function to handle incoming messages
def callback(ch, method, properties, body):
    print(f" [x] Received: {body}")

# Set up the consumer to receive messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# Start consuming messages
channel.start_consuming()
