import requests
import base64

# RabbitMQ Management API credentials
rabbitmq_host = 'localhost'  # Replace with your RabbitMQ server hostname or IP
rabbitmq_port = 15672        # Default RabbitMQ Management API port
rabbitmq_user = 'guest'      # Replace with your RabbitMQ username
rabbitmq_password = 'guest'  # Replace with your RabbitMQ password

# Create a session with authentication
session = requests.Session()
session.auth = (rabbitmq_user, rabbitmq_password)

# RabbitMQ Management API URL
api_url = f'http://{rabbitmq_host}:{rabbitmq_port}/api/queues'

# Send a GET request to fetch queue information
response = session.get(api_url)

# Check if the request was successful
if response.status_code == 200:
    queues = response.json()
    
    # Iterate through the list of queues and display detailed information
    for queue in queues:
        queue_name = queue['name']
        message_count = queue['messages']
        consumer_count = queue['consumers']
        
        print(f"Queue Name: {queue_name}")
        print(f"Message Count: {message_count}")
        print(f"Consumer Count: {consumer_count}")
        print("=" * 30)
else:
    print(f"Failed to fetch queue information. Status Code: {response.status_code}")

# Close the session
session.close()
