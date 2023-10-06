import subprocess

# List all Docker images including those associated with stopped containers
list_images_command = "docker images -q --all"
image_ids = subprocess.check_output(list_images_command, shell=True, universal_newlines=True).splitlines()

# Delete each Docker image
for image_id in image_ids:
    delete_image_command = f"docker rmi {image_id}"
    subprocess.run(delete_image_command, shell=True, check=True)

# Prune Docker resources (containers, networks, volumes)
prune_command = "docker system prune -a -f"
subprocess.run(prune_command, shell=True, check=True)

print("All Docker images, including those associated with stopped containers, have been deleted, and Docker resources have been pruned.")
