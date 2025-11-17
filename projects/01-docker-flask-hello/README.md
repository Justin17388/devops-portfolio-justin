# Dockerized Flask Hello

A simple Python Flask application containerized with Docker and automated with GitHub Actions. This project demonstrates the fundamentals of containerization, CI/CD, and deploying lightweight services for cloud or local environments.

# What This Project Demonstrates

Containerizing a Python web application using Docker
Building and running Docker images locally
Automated CI with GitHub Actions, including linting and build checks
Pushing Docker images to a registry (Docker Hub or GitHub Container Registry)
Best practices such as .dockerignore, image tagging, and clean container structure
Hands-on DevOps workflow: Build → Test → Package → Run

# Tech Stack

Language: Python 3
Framework: Flask
Containerization: Docker
CI/CD: GitHub Actions
Linting/Quality: flake8, pre-commit hooks

# Project Architecture

```bash
.
├── app.py              # Simple Flask application
├── Dockerfile          # Builds the container image
├── requirements.txt    # Python dependencies
├── .flake8             # Linting rules
├── .github/workflows/  # GitHub Actions CI pipeline
└── README.md
```

## How to Run the App Locally with Docker

```bash
docker build -t flask-hello-app .
docker run -p 80:80 flask-hello-app
```

# Visit the app

Open your browser:
http://localhost/

# GitHub Actions CI Pipeline

-Runs flake8 linting
-Builds the Docker image
-Optionally pushes the image to a container registry
-Ensures all pull requests pass checks before merging

# Real-World Use Case

-Packaging apps into portable containers
-Automating testing and builds
-Preparing services to run on ECS, EKS, EC2, or Kubernetes
-Standardizing deployments across environments

# Future Enhancements 

-Multi-stage builds to shrink image size
-Deployment to AWS ECS or EKS
-Terraform IaC to provision infrastructure
-A CloudWatch log configuration
-Docker Compose for multi-container apps
