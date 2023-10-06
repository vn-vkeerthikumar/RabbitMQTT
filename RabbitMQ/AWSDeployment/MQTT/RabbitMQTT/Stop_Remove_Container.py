import docker

# Initialize the Docker client
client = docker.from_env()

# List all containers (including stopped ones)
containers = client.containers.list(all=True)

# Stop and remove each container
for container in containers:
    container.stop()
    container.remove()

print("All Docker containers have been stopped and removed.")
