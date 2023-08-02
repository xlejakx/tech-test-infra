# Use the official Python image as the base image
FROM python:3

# Install Ansible
RUN pip install ansible

# Set the working directory inside the container
WORKDIR /ansible

# Copy your Ansible project files into the container
COPY . .

# Copy the private key file into the container
COPY rsa /root/.ssh/id_rsa

# Set the entrypoint script that accepts the playbook name as an argument
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]