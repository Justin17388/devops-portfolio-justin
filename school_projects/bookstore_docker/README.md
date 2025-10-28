# 📚 Bookstore Web API – Dockerized Flask + MySQL + Terraform (Project-203)

This project demonstrates the **end-to-end deployment** of a RESTful Bookstore API written in Python Flask, containerized with **Docker** and **Docker Compose**, and provisioned automatically on **AWS EC2** using **Terraform**.

---

## 🚀 Overview

The Bookstore API allows CRUD operations on a MySQL-backed database of books:

| Method | Endpoint | Description |
|---------|-----------|-------------|
| `GET` | `/books` | Retrieve all books |
| `GET` | `/books/<id>` | Retrieve a single book by ID |
| `POST` | `/books` | Add a new book |
| `PUT` | `/books/<id>` | Update a book |
| `DELETE` | `/books/<id>` | Delete a book |

---

## 🧩 Architecture
