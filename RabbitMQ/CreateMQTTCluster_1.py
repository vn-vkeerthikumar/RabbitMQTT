import subprocess
import time
import os

# Define the RabbitMQ cluster nodes and their ports
nodes = [
    {"name": "rabbit1", "port": 5672, "mgport" : 15672},
    {"name": "rabbit2", "port": 5673, "mgport" : 15673},
    {"name": "rabbit3", "port": 5674, "mgport" : 15674},
]

# Define the image name and tag
image_name = "my-rabbitmq-image"
image_tag = "1.0"

# create a network for cluster 
os.system("docker network create rabbitmq-network")


# Create Docker containers for each node
for node in nodes:
    container_name = node["name"]
    port = node["port"]
    managePort = node["mgport"]

    # Run RabbitMQ Docker container with the specified name and port
    subprocess.run(["docker", "run", "-d", "--hostname", container_name, "--name", container_name, "--network", "rabbitmq-network", "-p", f"{port}:5672", "-p", f"{managePort}:15672", "-e", "RABBITMQ_ERLANG_COOKIE='clustercookie'", "my-rabbitmq-image:1.0"])

    # Wait for the container to start (adjust sleep duration as needed)
    time.sleep(5)

# Configure each node to join the cluster
for i, node in enumerate(nodes):
    container_name = node["name"]
    cluster_nodes = [
        f"rabbit@{node['name']}" for node in nodes if node != nodes[i]
    ]

    # # Join the nodes into a cluster
    # for cluster_node in cluster_nodes:
    #     subprocess.run(["docker", "exec", container_name, "rabbitmqctl", "stop_app"])
    #     subprocess.run(["docker", "exec", container_name, "rabbitmqctl", "reset"])
    #     subprocess.run(["docker", "exec", container_name, "rabbitmqctl", "join_cluster", cluster_node])
    #     subprocess.run(["docker", "exec", container_name, "rabbitmqctl", "start_app"])

    # Join the nodes into a cluster
    for cluster_node in cluster_nodes:
        subprocess.run(["docker", "exec", "-it", container_name, "rabbitmqctl", "stop_app"])
        subprocess.run(["docker", "exec", "-it", container_name, "rabbitmqctl", "reset"])
        subprocess.run(["docker", "exec", "-it", container_name, "rabbitmqctl", "join_cluster", "rabbit@rabbit1"])
        subprocess.run(["docker", "exec", "-it", container_name, "rabbitmqctl", "start_app"])

print("RabbitMQ cluster has been created.")
