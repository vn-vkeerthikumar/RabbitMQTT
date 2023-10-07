import pika

# Connection parameters for RabbitMQ
connection_params = pika.ConnectionParameters(
    host='13.233.39.76',  # Change to the appropriate hostname or IP address if needed
    port=5672,
    credentials=pika.credentials.PlainCredentials('guest', 'guest')
)

# Establish a connection to RabbitMQ
connection = pika.BlockingConnection(connection_params)

# Create a channel
channel = connection.channel()

# Declare a queue (make sure it exists in RabbitMQ)
queue_name = '/event/1/user1@videonetics.com'
channel.queue_declare(queue=queue_name)

# Define a callback function to process incoming messages
def callback(ch, method, properties, body):
    print(f" [x] Received: {body}")

# Set up a consumer
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit, press Ctrl+C')
channel.start_consuming()
