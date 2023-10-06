import boto3
import time
import os

# AWS credentials and region
aws_access_key = 'YOUR_ACCESS_KEY'
aws_secret_key = 'YOUR_SECRET_KEY'
region = 'us-west-1'

# EC2 instance settings
instance_type = 't2.micro'
image_id = 'ami-12345678'  # Replace with the appropriate Amazon Linux AMI ID
key_name = 'your-key-pair'
security_group_ids = ['security-group-id']

# RabbitMQ cluster settings
rabbitmq_erlang_cookie = 'RABBITMQ_ERLANG_COOKIE'
rabbitmq_node_name = 'rabbit@node'
rabbitmq_cluster_nodes = ['rabbit@node1', 'rabbit@node2', 'rabbit@node3']

# Connect to AWS using boto3
ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)

# Launch EC2 instances
instance_ids = []
for i in range(len(rabbitmq_cluster_nodes)):
    response = ec2.run_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        KeyName=key_name,
        SecurityGroupIds=security_group_ids,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': f'RabbitMQ-Node{i+1}'}]
            }
        ]
    )
    instance_ids.append(response['Instances'][0]['InstanceId'])

print("Instances launched:", instance_ids)

# Wait for instances to be running
while True:
    instances = ec2.describe_instances(InstanceIds=instance_ids)
    all_running = all(state['Name'] == 'running' for state in instances['Reservations'][0]['Instances'][0]['State'])
    if all_running:
        break
    time.sleep(10)

print("All instances are running")

# SSH and execute commands on instances
for i, instance_id in enumerate(instance_ids):
    instance = instances['Reservations'][i]['Instances'][0]
    instance_ip = instance['PublicIpAddress']

    ssh_command = f"ssh -i 'path/to/your/key.pem' ec2-user@{instance_ip}"
    
    # Install Docker and RabbitMQ using ssh_command
    install_docker_command = "sudo yum install -y docker"
    start_docker_command = "sudo service docker start"
    install_rabbitmq_command = (
        "sudo docker run -d --rm --name rabbitmq "
        f"-e RABBITMQ_ERLANG_COOKIE='{rabbitmq_erlang_cookie}' "
        f"-e RABBITMQ_NODENAME='{rabbitmq_node_name}' "
        "-p 5672:5672 -p 15672:15672 "
        "rabbitmq:3-management"
    )
    
    ssh_commands = [
        install_docker_command,
        start_docker_command,
        install_rabbitmq_command
    ]
    
    for cmd in ssh_commands:
        full_command = f"{ssh_command} '{cmd}'"
        os.system(full_command)
        print(f"Executed command on instance {instance_id}: {cmd}")

print("Docker and RabbitMQ installation and configuration complete.")
