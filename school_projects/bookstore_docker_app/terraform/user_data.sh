#!/bin/bash
set -euxo pipefail

# These are Terraform template variables (get replaced by templatefile)
# Do NOT change the lowercase names here.
REPO_URL="${repo_url}"
APP_DIR="${app_dir}"

yum update -y
amazon-linux-extras enable docker || true
yum install -y docker git curl

systemctl enable docker
systemctl start docker

# Install Docker Compose v2
curl -L "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clone your repo
cd /home/ec2-user
git clone "$REPO_URL" apprepo

# Use $$ to escape Bash variable expansion in a Terraform template
cd "apprepo/$${APP_DIR}"

# Ensure .env exists on the instance (safe to overwrite for demos)
cat > .env <<'EOF'
MYSQL_ROOT_PASSWORD=ChangeMeRoot!
MYSQL_DATABASE=bookstore_db
MYSQL_USER=clarusway
MYSQL_PASSWORD=Clarusway_1
EOF

/usr/local/bin/docker-compose up -d
