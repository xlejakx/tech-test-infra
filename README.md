# infra-feedback

#### Assets provided

- `debian10-ssh.img.tar.xz`: Compressed disk image of a virtual machine. This can be [downloaded from this link](https://immfly-infra-technical-test.s3-eu-west-1.amazonaws.com/debian10-ssh.img.tar.xz)
- `vm.xml`: Virtual machine XML definition for `libvirt`
- `rsa`: Authorized RSA key for accessing the virtual machine
- `index.html`: Frontend clock application

## VM import
I use `Proxmox` as Hypervisor, and there are some additional important steps involved.
~~~bash
    scp debian10-ssh.img.tar.xz vm@10.99.0.100:/opt/debian.tar.xz
    tar -xf debian.tar.xz
    qm create <VM_ID> --name immfly-debian10 --memory 1024 --net0 virtio,bridge=vmbr0 --cores 1
    qm importdisk <VM_ID> debian10-ssh.img local-zfs
    qm set <VM_ID> --scsihw virtio-scsi-pci --scsi0 local-zfs:vm-<DISK_ID>/disk-<DISK_ID>.img --boot c
~~~
Upon further investigation, I discovered that the machine is unable to obtain an IP address, consequently preventing me from establishing a connection to the instance.
~~~
It will try to configure it's network interface via DHCP.
~~~
It seems that the key is present. I proceeded by resetting the root password and fixing the mismatched network interface name. As a result, the machine is now online and functioning properly.

## Application
I'm not a huge fan of Python, but since it's already installed, I made use of it.
  
[x] Implement backend service (using any language/tech you love... or hate)
~~~python
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/clock':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            timestamp = str(time.time()).encode('utf-8')
            self.wfile.write(timestamp)
        else:
            super().do_GET()
~~~

## Ansible
I didn't do anything special; I simply wrote the playbook as required.

[x] Use ansible to deploy frontend and backend services inside the virtual machine.
~~~bash
    ansible-playbook playbooks/infra.yml
~~~

## Extra points

- Proper ansible project structure
- Use docker to run ansible
- Use ssh-agent inside ansible container
- Run frontend and backend services using docker
- Backend application configurable using environment variables
- Don't run services as root
- Configure & deploy **EVERYTHING** using a single command, i.e: bash script

### Proper ansible project structure
~~~bash
├── ansible.cfg
├── files
│   └── app
│       ├── app.py
│       └── index.html
├── inventories
│   ├── group_vars
│   └── production
│       ├── group_vars
│       │   └── all.yml
│       └── hosts.ini
├── playbooks
│   ├── infra.yml
│   └── kill.yml
├── roles
│   ├── killer
│   │   └── tasks
│   │       └── main.yml
│   └── webserver
│       └── tasks
│           └── main.yml
└── tamplates
~~~

### Use docker to run ansible
Never used this method before, but if requested. 
~~~bash
docker run -it --rm -v .:/ansible ansible infra.yml
~~~

### Use ssh-agent inside ansible container
Done. 
~~~bash
ansible.cfg
ssh_args = -o ForwardAgent=yes

entrypoint.sh
# Start the ssh-agent and add the private key(s) to it
eval $(ssh-agent)
ssh-add /root/.ssh/id_rsa
~~~

### Run frontend and backend services using docker
~~~docker
# Use the official Python image as the base image
FROM python:3

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the app dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY files/app/ .

# Expose the port on which your Python app listens
EXPOSE 80

# Define the command to run your Python app (replace 'app.py' with your app's main Python file)
CMD ["python", "app.py"]
~~~

### Backend application configurable using environment variables
My backup is simple, but why not. Now `PORT` is variable.

### Don't run services as root
Agree, better use toor