import os
import subprocess

# Define the names and IP addresses of your VMs
vm_info = [
    {"name": "vm1", "ip": "vm1_ip_address"},
    {"name": "vm2", "ip": "vm2_ip_address"},
    {"name": "vm3", "ip": "vm3_ip_address"}
]

# SSH username and private key file path
ssh_username = "your_ssh_username"
ssh_key_path = "Path To SSh Keys"

# Step 1: Install Docker and Docker Compose on each VM
for vm in vm_info:
    vm_name = vm["name"]
    vm_ip = vm["ip"]

    print(f"Installing Docker and Docker Compose on {vm_name}...")

    # Install Docker
    install_docker_command = f"ssh -i {ssh_key_path} {ssh_username}@{vm_ip} 'sudo apt-get update && sudo apt-get install -y docker.io'"
    subprocess.run(install_docker_command, shell=True)

    # Install Docker Compose
    install_compose_command = f"ssh -i {ssh_key_path} {ssh_username}@{vm_ip} 'sudo curl -L 'https://github.com/docker/compose/releases/latest/download/docker-compose-Linux-x86_64' -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose'"
    subprocess.run(install_compose_command, shell=True)

# Step 2: Download MQTT Docker image and create a Swarm cluster
mqtt_image = "eclipse-mosquitto:latest"

# Initialize Docker Swarm on the first VM
init_swarm_command = f"ssh -i {ssh_key_path} {ssh_username}@{vm_info[0]['ip']} 'sudo docker swarm init --advertise-addr {vm_info[0]['ip']}'"
subprocess.run(init_swarm_command, shell=True)

# Get the join token from the first VM
join_token_command = f"ssh -i {ssh_key_path} {ssh_username}@{vm_info[0]['ip']} 'sudo docker swarm join-token worker -q'"
join_token = subprocess.check_output(join_token_command, shell=True, text=True).strip()

# Join the other VMs to the Swarm
for vm in vm_info[1:]:
    join_swarm_command = f"ssh -i {ssh_key_path} {ssh_username}@{vm['ip']} 'sudo docker swarm join --token {join_token} {vm_info[0]['ip']}:2377'"
    subprocess.run(join_swarm_command, shell=True)

# Step 3: Deploy MQTT Docker stack with management console
mqtt_stack = """
version: '3.7'
services:
  mqtt:
    image: eclipse-mosquitto
    ports:
      - "1883:1883"
      - "9001:9001"
    deploy:
      replicas: 3
"""
with open("mqtt-stack.yml", "w") as stack_file:
    stack_file.write(mqtt_stack)

deploy_stack_command = f"scp -i {ssh_key_path} mqtt-stack.yml {ssh_username}@{vm_info[0]['ip']}:/tmp/mqtt-stack.yml && ssh -i {ssh_key_path} {ssh_username}@{vm_info[0]['ip']} 'sudo docker stack deploy --compose-file /tmp/mqtt-stack.yml mqtt'"
subprocess.run(deploy_stack_command, shell=True)

# Cleanup: Remove the local stack file
os.remove("mqtt-stack.yml")

print("MQTT cluster with management console is deployed successfully.")
