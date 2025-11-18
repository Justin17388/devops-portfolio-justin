# Project 3 — Automated Flask App Deployment with Ansible, Docker, and EC2

This project demonstrates a full end-to-end automated deployment pipeline using **Ansible**, **Docker**, and **AWS EC2**. The goal is to provision a remote Linux server with Docker, pull a container image from `ghcr.io`, and run it as a managed **systemd service**—fully automated through Infrastructure-as-Code.

This project is part of my DevOps portfolio, showcasing real-world configuration management, secrets handling, and container orchestration skills.

---

## 🚀 Architecture Overview

Local Ansible Control Node (WSL)
|
| SSH + Ansible Playbook
v
AWS EC2 Instance (Amazon Linux)
|
├── Install Docker
├── Pull GHCR image: flask-hello
├── Run container on port 80
└── Manage lifecycle via systemd

The deployed application is a simple Flask API that returns:


---

## 📁 Project Structure

03-ansible-flask-docker/
│
├── inventory/
│ └── hosts.ini # Points to EC2 instance
│
├── group_vars/
│ └── all.yml # App variables (image, ports)
│
├── roles/
│ ├── docker/ # Docker installation automation
│ │ └── tasks/main.yml
│ └── app/ # Deploy & manage the app container
│ └── tasks/main.yml
│
├── templates/
│ └── flask-hello.service.j2 # systemd service file template
│
├── site.yml # Main Ansible playbook
└── README.md


---

## 🔐 Secrets & Inventory Management

Secrets (private EC2 key, vaulted variables, etc.) are stored in a **separate private repository**:

ansible-secrets/

This repo contains:

- `inventories/prod/hosts.ini`
- `group_vars/all/vault.yml` (encrypted)
- `ansible.cfg` pointing to local vault password file

Sensitive data is **never committed** to the portfolio repo.

---

## ⚙️ Variables

Group variables for this deployment are defined in:

group_vars/all.yml

Example:

```yaml
app_name: flask-hello
container_image: "ghcr.io/justin17388/flask-hello:latest"
container_port: 5000
host_port: 80

🧩 Key Features
✔ Automated provisioning

Install Docker on EC2 depending on OS family (Amazon Linux or Ubuntu).

✔ Pull image from GHCR

Uses a public image from GitHub Container Registry.

✔ Deploy container as a systemd service

Ensures the app:

always starts on boot

restarts on failure

runs under a stable name (flask-hello)

✔ Secrets externalized

Private SSH key stays in ~/.ssh/
Sensitive vars stored in an encrypted Vault file.

✔ Real-world deployment flow

Just like a production CI/CD pipeline using IaC.

▶️ How to Run the Deployment

1. Ensure SSH access works

ssh -i ~/.ssh/YOUR-KEY.pem ec2-user@YOUR-PUBLIC-IP

2. Test Ansible connectivity

From repo root:

ansible -i ../ansible-secrets-justin/inventories/prod/hosts.ini web -m ping

You should see: "ping": "pong"

3. Deploy the application

ansible-playbook \
  -i ../ansible-secrets-justin/inventories/prod/hosts.ini \
  projects/03-ansible-flask-docker/site.yml

🌐 Accessing the Application

Open your browser:

http://YOUR-EC2-PUBLIC-IP/

You should see:

Hello from Flask!

🛠 Troubleshooting

❌ invalid reference format

Docker image name must be lowercase:

ghcr.io/justin17388/flask-hello:latest

❌ App loads locally but not in browser

Check EC2 Security Group:

Inbound rule: HTTP (80) → 0.0.0.0/0

❌ App not running

Check systemd status:

sudo systemctl status flask-hello
sudo docker ps

❌ Container restarts repeatedly

Check logs:

sudo journalctl -u flask-hello -n 100 --no-pager

🏁 Result

Using Ansible automation, the Flask container is now:

deployed automatically

managed with systemd

publicly reachable

reproducible

entirely defined as code

This project demonstrates real DevOps skills in configuration management, secret handling, containerization, and cloud deployment.

📌 Future Enhancements

Add GitHub Actions workflow:
→ Auto-run Ansible on push or manual trigger

Add Blue/Green deployment example

Add monitoring (Prometheus + Grafana)

Convert EC2 to Terraform-provisioned infrastructure

📚 Technologies Used

Ansible

Docker

AWS EC2

GitHub Container Registry (GHCR)

Python / Flask

Systemd

Ansible Vault

WSL2 (Ubuntu)

Author: Justin Shinn
DevOps Engineer in training — AWS, Docker, Terraform, CI/CD
