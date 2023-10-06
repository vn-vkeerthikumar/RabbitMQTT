import pika

# Connection parameters for RabbitMQ
connection_params = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    credentials=pika.credentials.PlainCredentials('guest', 'guest')
)

# Establish a connection to RabbitMQ
connection = pika.BlockingConnection(connection_params)

# Create a channel
channel = connection.channel()

# Declare a queue (make sure it exists in RabbitMQ)
queue_name = 'TestMQTT'
channel.queue_declare(queue=queue_name)

# Publish a message
message = "Hello, RabbitMQ Cluster!"
channel.basic_publish(exchange='', routing_key=queue_name, body=message)

print(f" [x] Sent: {message}")

# Close the connection
connection.close()
