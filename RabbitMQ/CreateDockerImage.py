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
image_name = "my-rabbitmq-image"
image_tag = "1.0"

# Define the Dockerfile path (for writing to a temporary file)
dockerfile_path = "D:\\RabbitMQ\\Dockerfile"

# Write the Dockerfile content to a temporary file
with open(dockerfile_path, "w") as dockerfile:
    dockerfile.write(dockerfile_content)

# Build the Docker image
build_command = f"docker build -t {image_name}:{image_tag} -f {dockerfile_path} ."
subprocess.run(build_command, shell=True, check=True)

# Run the Docker image as a container
#run_command = f"docker run -d --name {image_name}-{image_tag} {image_name}:{image_tag}"
run_command = f"docker run -d --name {image_name}-{image_tag} -p 15672:15672 -p 5672:5672 {image_name}:{image_tag}"
subprocess.run(run_command, shell=True, check=True)

print(f"Docker container {image_name}-{image_tag} is running.")
