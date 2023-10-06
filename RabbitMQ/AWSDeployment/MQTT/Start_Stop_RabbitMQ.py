import subprocess

# Stop the RabbitMQ cluster
stop_command = "docker-compose -f rabbitmq-cluster/docker-compose.yml down"
subprocess.run(stop_command, shell=True)

# Start the RabbitMQ cluster
start_command = "docker-compose -f rabbitmq-cluster/docker-compose.yml up -d"
subprocess.run(start_command, shell=True)

print("RabbitMQ cluster is stopped and started successfully.")
