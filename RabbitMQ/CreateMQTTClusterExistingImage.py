import os

# Define the Docker Compose configuration in YAML format
docker_compose_yaml = """
version: '3'
services:
  rabbit1:
    image: my-rabbitmq-image:1.0
    hostname: rabbit1
    environment:
      - RABBITMQ_ERLANG_COOKIE=mycookie
    ports:
      - "5672:5672"
      - "15672:15672"
    networks:
      - rabbitmq-net
  rabbit2:
    image: my-rabbitmq-image:1.0
    hostname: rabbit2
    environment:
      - RABBITMQ_ERLANG_COOKIE=mycookie
    ports:
      - "5673:5672"
      - "15673:15672"
    networks:
      - rabbitmq-net
    command: rabbitmq-server
    depends_on:
      - rabbit1
  rabbit3:
    image: my-rabbitmq-image:1.0
    hostname: rabbit3
    environment:
      - RABBITMQ_ERLANG_COOKIE=mycookie
    ports:
      - "5674:5672"
      - "15674:15672"
    networks:
      - rabbitmq-net
    command: rabbitmq-server
    depends_on:
      - rabbit1
networks:
  rabbitmq-net:
"""

# Create a Docker Compose YAML file
with open('docker-compose.yml', 'w') as f:
    f.write(docker_compose_yaml)

# Create a Docker network
os.system('docker network create rabbitmq-net')

# Run Docker Compose to start the RabbitMQ cluster
os.system('docker-compose up -d')

print("RabbitMQ cluster with existing image 'my-rabbitmq-image:1.0' is running.")
