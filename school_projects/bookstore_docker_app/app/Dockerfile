FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps so the MySQLdb driver (mysqlclient) can compile if pulled by flask-mysql
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential default-libmysqlclient-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Use the class-provided requirements exactly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Your class-provided Flask app (binds to port 80 and connects to service 'database')
COPY bookstore-api.py .

EXPOSE 80
CMD ["python", "bookstore-api.py"]
