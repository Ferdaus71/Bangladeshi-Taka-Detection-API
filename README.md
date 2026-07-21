# 🇧🇩 Bangladeshi Taka Note Detection API

<div align="center">

<img src="https://raw.githubusercontent.com/Ferdaus71/Bangladeshi-Taka-Detection-API/main/assets/banner.png" alt="Banner" width="100%">

### 🚀 Production-Ready FastAPI REST API for Bangladeshi Banknote Detection using YOLOv11

Detect Bangladeshi currency notes with high accuracy using a YOLOv11 deep learning model exposed through a modern FastAPI backend.

<p>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![YOLOv11](https://img.shields.io/badge/YOLOv11-Ultralytics-red?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Supported-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

</p>

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/Ferdaus71/Bangladeshi-Taka-Detection-API)
[![API Docs](https://img.shields.io/badge/API-Swagger-success?style=for-the-badge&logo=swagger)](http://localhost:8000/docs)
[![Author](https://img.shields.io/badge/Author-Md.%20Ferdaus%20Hossen-blue?style=for-the-badge)](https://github.com/Ferdaus71)

</div>

---

# 📖 Overview

The **Bangladeshi Taka Note Detection API** is a production-ready REST API that detects Bangladeshi banknotes from images using a **YOLOv11 Object Detection model**.

The system provides an easy-to-use API that enables developers to integrate Bangladeshi currency recognition into web applications, mobile apps, ATM automation, smart payment systems, vending machines, and financial technology solutions.

The API is developed with **FastAPI**, ensuring high performance, automatic API documentation, asynchronous request handling, and scalable deployment.

---

# 🎯 Project Objectives

The project aims to:

- Detect Bangladeshi Taka notes from uploaded images
- Recognize multiple banknotes simultaneously
- Return denomination, confidence score, and bounding boxes
- Provide a modern REST API
- Support batch prediction
- Offer Docker deployment
- Enable cloud deployment (Render, Railway, Azure, AWS)
- Deliver production-ready documentation

---

# ✨ Key Features

## 💰 Currency Detection

- Detect Bangladeshi banknotes
- Multiple note detection
- High-confidence predictions
- Fast inference
- Bounding box localization

---

## ⚡ REST API

- FastAPI backend
- OpenAPI support
- Swagger UI
- ReDoc documentation
- Async endpoints
- JSON responses

---

## 🧠 AI Model

- YOLOv11 Object Detection
- PyTorch
- Ultralytics Framework
- GPU support
- CPU inference

---

## 🚀 Production Ready

- Docker support
- Docker Compose
- Health monitoring
- Structured logging
- Environment configuration
- Error handling
- Input validation

---

# 💵 Supported Denominations

| Class | Denomination |
|--------|--------------|
| 0 | 10 Taka |
| 1 | 20 Taka |
| 2 | 50 Taka |
| 3 | 100 Taka |
| 4 | 200 Taka |
| 5 | 500 Taka |
| 6 | 1000 Taka |

---

# 🛠 Technology Stack

| Category | Technology |
|-----------|------------|
| Backend | FastAPI |
| Programming Language | Python |
| AI Framework | Ultralytics |
| Model | YOLOv11 |
| Deep Learning | PyTorch |
| Image Processing | OpenCV |
| Validation | Pydantic |
| API Server | Uvicorn |
| Containerization | Docker |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```text
Bangladeshi-Taka-Detection-API/
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── predictor.py
│   ├── schemas.py
│   ├── config.py
│   ├── utils.py
│   └── main.py
│
├── model/
│   └── best.pt
│
├── uploads/
├── outputs/
├── tests/
├── screenshots/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .env.example
```

---

# 📷 Screenshots

## Swagger UI

> Replace with your screenshot

```text
screenshots/swagger.png
```

---

## Prediction Example

> Replace with your screenshot

```text
screenshots/prediction.png
```

---

# 📈 Workflow

```text
Client
   │
   ▼
FastAPI Endpoint
   │
   ▼
Image Validation
   │
   ▼
YOLOv11 Model
   │
   ▼
Prediction
   │
   ▼
JSON Response
```

---

# 📌 Highlights

- ✅ Production Ready
- ✅ RESTful API
- ✅ FastAPI
- ✅ YOLOv11
- ✅ Docker Support
- ✅ Batch Prediction
- ✅ Swagger Documentation
- ✅ High Accuracy
- ✅ Easy Deployment
- ✅ Scalable Architecture

---

➡️ **Part 2** will include:

- Installation Guide
- Windows Setup
- Linux Setup
- Docker Installation
- Environment Variables
- Running the API
- Swagger UI
- Health Check
- Quick Start
