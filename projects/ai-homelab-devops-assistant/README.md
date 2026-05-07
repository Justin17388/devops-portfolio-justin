# 🧠 Self-Hosted AI DevOps Assistant Homelab

## Overview
This project documents the conversion of a legacy Sony Vaio laptop into a fully functional Linux-based AI homelab server. The system hosts a locally running large language model (LLM) for coding assistance and infrastructure troubleshooting, accessible via a web interface across the local network.

The goal was to create a cost-effective, private AI assistant while gaining hands-on experience with Linux, Docker, networking, and system administration.

---

## 🔧 Tech Stack

- **OS:** Linux Mint XFCE  
- **Containerization:** Docker  
- **AI Backend:** Ollama  
- **Web Interface:** Open WebUI  
- **Networking:** Local LAN access  
- **System Optimization:** Swap + zRAM  

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

---

## 📈 Future Improvements

- Reverse proxy with Nginx
- HTTPS with Let's Encrypt
- Authentication hardening
- Remote access via VPN or tunneling
- Automated log ingestion and analysis
- Monitoring stack (Prometheus + Grafana)

---

## 💡 Summary

This project demonstrates the ability to design, deploy, and troubleshoot a full-stack, self-hosted system using real-world DevOps practices. It highlights hands-on experience with infrastructure, containers, networking, and AI integration on constrained hardware.
