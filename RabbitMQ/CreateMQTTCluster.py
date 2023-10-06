import subprocess
import time

# Define the image name and tag
image_name = "my-rabbitmq-image"
image_tag = "1.0"

# Define the number of nodes in the cluster
num_nodes = 3  # You can change this to the desired number of nodes

# Create a list to store container names
container_names = []

# Create and run containers for the cluster
for i in range(num_nodes):
    container_name = f"{image_name}-{image_tag}-node-{i}"
    # run_command = f"docker run -d --name {container_name} {image_name}:{image_tag}"
    run_command = f"docker run -d --name {image_name}-{image_tag} -p 15672:15672 -p 5672:5672 {image_name}:{image_tag}"
    subprocess.run(run_command, shell=True, check=True)
    container_names.append(container_name)

print(f"Created {num_nodes} RabbitMQ containers.")

# Wait for containers to start (adjust the delay as needed)
time.sleep(10)

# Configure the RabbitMQ cluster
for i in range(1, num_nodes):
    source_node = container_names[0]
    target_node = container_names[i]
    
    # Join the target node to the cluster
    cluster_command = f"docker exec -it {source_node} rabbitmqctl stop_app && " \
                      f"docker exec -it {source_node} rabbitmqctl join_cluster rabbit@{target_node} && " \
                      f"docker exec -it {source_node} rabbitmqctl start_app"
    
    subprocess.run(cluster_command, shell=True, check=True)
    
    print(f"Node {target_node} joined the RabbitMQ cluster.")

print("RabbitMQ cluster is ready.")
