#!/bin/bash

export ANSIBLE_HOST_KEY_CHECKING=False

# Start the ssh-agent and add the private key(s) to it
eval $(ssh-agent)
ssh-add /root/.ssh/id_rsa

# Use the first argument as the playbook name, or use a default value (e.g., infra.yml)
PLAYBOOK_NAME=${1:-infra.yml}

# Run the ansible-playbook command with the specified playbook
ansible-playbook playbooks/"$PLAYBOOK_NAME"

# Stop the ssh-agent when the container is done
eval $(ssh-agent -k)