import subprocess

# Define the Dockerfile content
dockerfile_content = """
FROM rabbitmq:3.7.4

RUN rabbitmq-plugins enable --offline rabbitmq_management
RUN rabbitmq-plugins enable --offline rabbitmq_mqtt
RUN rabbitmq-plugins enable --offline rabbitmq_web_mqtt
RUN rabbitmq-plugins enable --offline rabbitmq_stomp
RUN rabbitmq-plugins enable --offline rabbitmq_web_stomp
"""

# Define the image name and tag
image_name = "rabbitmqtt-image"
image_tag = "1.0"

# Define the Dockerfile path (for writing to a temporary file)
dockerfile_path = "/home/ubuntu/MQTT/Dockerfile"

# Write the Dockerfile content to a temporary file
with open(dockerfile_path, "w") as dockerfile:
    dockerfile.write(dockerfile_content)

# Build the Docker image
build_command = f"sudo docker build -t {image_name}:{image_tag} -f {dockerfile_path} ."
subprocess.run(build_command, shell=True, check=True)

print(f"Docker image {image_name}:{image_tag} has been created.")
