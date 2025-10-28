# 📱 Phonebook App (Terraform + Flask + Docker + AWS)

A **cloud-deployed full-stack phonebook application** built with **Flask (Python)** and **MySQL**, containerized with **Docker**, and deployed to **AWS EC2** with **Terraform** infrastructure as code.

This project demonstrates practical DevOps and Cloud Engineering concepts including:
- Infrastructure automation with Terraform
- Application containerization using Docker
- Load balancing and networking on AWS
- CI/CD-ready architecture for future automation

---

## 🌍 Architecture Overview

```
User → AWS Application Load Balancer → EC2 Instance (Docker + Flask)
                                      ↳ MySQL (local or RDS)
```

**Infrastructure Components**
- **Terraform** provisions:
  - VPC, subnets, and security groups
  - EC2 instance for application hosting
  - Application Load Balancer (ALB)
  - Optional RDS MySQL instance
- **Flask Application** handles HTTP requests and interacts with the MySQL database.
- **Docker** containerizes the Flask app for easy deployment and consistency.
- **S3 + DynamoDB** backend stores Terraform remote state and locking.

---

## 🧩 Features

- Create, view, update, and delete phonebook entries.
- Backend database: MySQL (local or RDS).
- Frontend served via Flask templates.
- Dockerized for portability and reproducibility.
- Deployed through Terraform on AWS.

---

## ⚙️ Technologies Used

| Category | Tools |
|-----------|-------|
| **Cloud** | AWS (EC2, S3, ALB, DynamoDB, RDS) |
| **IaC** | Terraform |
| **Backend** | Python, Flask |
| **Database** | MySQL |
| **Containerization** | Docker |
| **OS** | Amazon Linux 2 / Ubuntu |
| **Monitoring** | CloudWatch (optional) |

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Justin17388/phonebook.git
cd phonebook
```

### 2️⃣ Configure Environment Variables
Create a `.env` file or export variables:
```bash
export DB_USER='phonebook_user'
export DB_PASSWORD='StrongPass!123'
export DB_NAME='phonebook'
export DB_HOST='localhost'    # or your RDS endpoint
```

### 3️⃣ Build and Run the Container
```bash
docker build -t phonebook-app .
docker run -d -p 5000:5000 --env-file .env phonebook-app
```

Access locally:
```
http://localhost:5000
```

---

## ☁️ Deploying to AWS with Terraform

### Initialize and apply:
```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

Once deployment completes, find your ALB DNS name:
```bash
terraform output alb_dns_name
```
Visit:
```
http://<alb-dns-name>
```

---

## 🧠 Health Check

The Flask app includes a health route:
```
/health → returns “ok” with status 200
```
Used by AWS ALB to verify instance health.

---

## 📂 Project Structure

```
phonebook/
│
├── app/                   # Flask application files
│   ├── phonebook-app.py
│   ├── templates/
│   ├── static/
│   └── requirements.txt
│
├── Dockerfile             # Builds the app image
├── terraform/             # Terraform IaC for AWS infra
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── backend.tf
│
├── .gitignore
└── README.md
```

---

## 🧰 Useful Commands

| Action | Command |
|--------|----------|
| Start container | `docker run -d -p 5000:5000 phonebook-app` |
| Stop container | `docker stop $(docker ps -q)` |
| Show logs | `docker logs <container_id>` |
| Destroy AWS infra | `terraform destroy -auto-approve` |

---

## 🧩 Future Improvements

- Add CI/CD with GitHub Actions
- Migrate database to Amazon RDS
- Add HTTPS via ACM + CloudFront
- Deploy container on ECS Fargate or EKS
- Implement CloudWatch logging & alarms

---
