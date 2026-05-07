# 🧠 Self-Hosted AI DevOps Assistant Homelab

## Overview

This project transforms a legacy Sony Vaio laptop into a self-hosted AI-powered DevOps homelab server. The system runs a locally hosted large language model (LLM) using Ollama, paired with a Dockerized Open WebUI frontend for browser-based interaction.

The platform enables private, cost-free AI-assisted coding and log analysis while demonstrating hands-on experience with Linux system administration, containerization, networking, and service configuration. Remote access is securely provided through Tailscale, allowing the system to function as a lightweight, always-on infrastructure node accessible from anywhere.

---

## 🔧 Tech Stack

### 🖥️ Infrastructure & OS
- Linux Mint XFCE (lightweight desktop environment)
- Sony Vaio E Series (repurposed legacy hardware)

### 🐳 Containerization & Services
- Docker
- Open WebUI (containerized frontend)

### 🧠 AI / Machine Learning
- Ollama (local LLM runtime)
- qwen2.5-coder / tinyllama (local models)

### 🌐 Networking & Remote Access
- Tailscale (secure remote access VPN)
- Local LAN networking
- SSH (OpenSSH server)

### ⚙️ System Optimization
- Swap (virtual memory expansion)
- zRAM (compressed memory)

### 🛠️ System Management
- systemd (service management)
- Bash / Linux CLI

---

## 🏗️ Architecture
Client Browser (LAN)
↓
Open WebUI (Docker Container)
↓
Ollama (Local Service)
↓
LLM Model (qwen2.5-coder / tinyllama)

---

## 🚀 Features

- Self-hosted AI assistant (no external API required)
- Browser-based interface accessible across local network
- Coding and log analysis capabilities
- Persistent services with auto-restart
- Optimized for low-memory hardware
- Headless operation (lid closed, remote access)
- Secure remote access via Tailscale
- Browser-based AI interface accessible from anywhere
  
---

## 🧪 Key Learning Areas

- Linux system installation and configuration
- Troubleshooting BIOS/bootloader issues
- Memory optimization using swap and zRAM
- Docker container deployment and management
- Debugging container-to-host networking
- Service management with systemd
- Local AI model hosting and inference

---

## ⚙️ Challenges & Solutions

### ❌ Open WebUI could not connect to Ollama
- **Cause:** Ollama bound to localhost only
- **Fix:** Configured systemd override to bind to `0.0.0.0`

### ❌ Docker container unable to resolve host
- **Cause:** Missing host mapping
- **Fix:** Added `--add-host=host.docker.internal:host-gateway`

### ❌ Model not appearing in WebUI
- **Cause:** API connection failure / UI cache
- **Fix:** Restarted services and forced connection refresh

---

## 📸 Screenshots

### Web Interface
![Web UI](images/webui-running.png)

### Docker Containers
![Docker](images/docker-containers.png)

### System Monitoring
![System Usage](images/system-usage.png)

### Ollama Models
![Models](images/ollama-model.png)

### Remote SSH Access
![SSH](images/ssh-access.png)

---

## 📈 Future Improvements

### 🌐 Networking & Access
- Implement Nginx reverse proxy for cleaner routing and service management
- Configure HTTPS using Let's Encrypt for secure browser access
- Expand secure remote access with domain-based routing and access control

### 🔐 Security & Hardening
- Implement authentication layer for Open WebUI access
- Transition SSH to key-based authentication and disable password login
- Apply firewall rules and service-level access restrictions

### 🧠 AI & Automation
- Integrate automated log ingestion for real-time analysis
- Develop scripts to feed system and application logs into the LLM
- Explore lightweight model optimization for improved performance on low-resource hardware

### 📊 Observability & Monitoring
- Deploy Prometheus and Grafana for system and container monitoring
- Track CPU, memory, and service health metrics
- Implement alerting for system thresholds and service failures

### ⚙️ Infrastructure Evolution
- Containerize additional services for modular expansion
- Convert system into a fully headless, always-on homelab node
- Explore multi-node expansion using additional devices connected via Tailscale

---

## 💡 Summary

This project demonstrates the ability to design, deploy, and troubleshoot a full-stack, self-hosted system using real-world DevOps practices. It highlights hands-on experience with infrastructure, containers, networking, and AI integration on constrained hardware.
