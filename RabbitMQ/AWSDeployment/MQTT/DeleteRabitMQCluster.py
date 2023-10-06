import subprocess

# Navigate to the directory containing the docker-compose.yml file
docker_compose_dir = "/home/ubuntu/MQTT/rabbitmq-cluster"

# Stop and remove the RabbitMQ containers
stop_and_remove_command = f"docker-compose -f {docker_compose_dir}/docker-compose.yml down"
subprocess.run(stop_and_remove_command, shell=True)

#  Prune Docker resources (containers, networks, volumes)
prune_command = "docker system prune -f"
subprocess.run(prune_command, shell=True)

print("RabbitMQ cluster has been deleted, and Docker resources have been pruned.")
