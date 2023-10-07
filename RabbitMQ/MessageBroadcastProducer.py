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

# Declare a fanout exchange
exchange_name = '/event/1/user1@videonetics.com'
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

# Publish a message to the fanout exchange (which will broadcast to all queues bound to it)
message = "Hello, RabbitMQ Cluster!"
channel.basic_publish(exchange=exchange_name, routing_key='', body=message)

print(f" [x] Sent: {message}")

# Close the connection
connection.close()
