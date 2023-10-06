import subprocess

# Define the Docker Compose YAML configuration for the RabbitMQ cluster
docker_compose_config = """
version: '3'
services:
  rabbitmq1:
    image: rabbitmq:latest
    hostname: rabbit1
    ports:
      - "5673:5672"
      - "15672:15672"
    environment:
      - RABBITMQ_ERLANG_COOKIE=my-secret-cookie
      - RABBITMQ_DEFAULT_USER=admin
      - RABBITMQ_DEFAULT_PASS=adminpass
    networks:
      - rabbitmq-cluster

  rabbitmq2:
    image: rabbitmq:latest
    hostname: rabbit2
    environment:
      - RABBITMQ_ERLANG_COOKIE=my-secret-cookie
    networks:
      - rabbitmq-cluster
    depends_on:
      - rabbitmq1

  rabbitmq3:
    image: rabbitmq:latest
    hostname: rabbit3
    environment:
      - RABBITMQ_ERLANG_COOKIE=my-secret-cookie
    networks:
      - rabbitmq-cluster
    depends_on:
      - rabbitmq1

networks:
  rabbitmq-cluster:
"""

# Create a directory for the RabbitMQ cluster and write the Docker Compose config to a file
subprocess.run("mkdir -p rabbitmq-cluster", shell=True)
with open("rabbitmq-cluster/docker-compose.yml", "w") as docker_compose_file:
    docker_compose_file.write(docker_compose_config)

# Start the RabbitMQ cluster using Docker Compose
subprocess.run("docker-compose -f rabbitmq-cluster/docker-compose.yml up -d", shell=True)

# Enable the RabbitMQ management console on the first node
enable_management_console_command = (
    "docker exec -it rabbitmq-cluster_rabbitmq1_1"
    "rabbitmq-plugins enable --offline rabbitmq_management"
    #"rabbitmq-plugins enable --offline rabbitmq_mqtt"
    #"rabbitmq-plugins enable --offline rabbitmq_web_mqtt"
    #"rabbitmq-plugins enable --offline rabbitmq_stomp"
    #"rabbitmq-plugins enable --offline rabbitmq_web_stomp"
)
subprocess.run(enable_management_console_command, shell=True)

print("RabbitMQ cluster with management console is created successfully.")
