# 🚀 SupplyNet 360
### AI-Powered Inventory & Demand Forecasting Suite

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![CI](https://github.com/MoonlitEcho/supplyNet360/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/MoonlitEcho/supplyNet360/actions/workflows/cd.yml/badge.svg)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

SupplyNet 360 is an end-to-end machine learning system for demand forecasting and inventory optimization. It combines time-series modeling, modular ML pipelines, and an interactive dashboard to help businesses make data-driven supply chain decisions.

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Results](#-results)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 📌 Overview

Efficient inventory management requires accurate demand forecasting. SupplyNet 360 solves this by building a scalable ML pipeline that:

- Processes historical demand data
- Engineers time-based features
- Trains forecasting models
- Serves predictions via REST APIs
- Visualizes insights in real time

---

## ✨ Features

### 🔮 Demand Forecasting
- Time-series forecasting using statistical/ML models
- Multi-step future predictions
- Captures trends, seasonality, and anomalies

### ⚙️ Model Serving
- FastAPI-based REST endpoints
- Real-time inference support
- Scalable backend design

### 📊 Interactive Dashboard
- Built with Streamlit
- Forecast vs. actual demand visualization
- Confidence intervals and trend patterns

### 🧩 Modular ML Pipeline
- Separation of data preprocessing, feature engineering, model training, and inference
- Enables reproducibility and rapid experimentation

---

## 🏗️ System Architecture

```
Raw Data
   ↓
Data Preprocessing (Pandas)
   ↓
Feature Engineering (Time-based)
   ↓
Model Training (Prophet / ARIMA)
   ↓
FastAPI Inference Service
   ↓
Streamlit Dashboard (Visualization)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.8+ |
| Data Processing | Pandas, NumPy |
| ML Models | Prophet, ARIMA (Statsmodels) |
| Backend API | FastAPI |
| Visualization | Streamlit |
| Deployment (Planned) | Docker, AWS |

---

## 📂 Project Structure

```
supplynet360/
│
├── .streamlit/               # Streamlit configuration
├── Deploy/                   # Deployment scripts & configs
├── outputs_final_model/      # Trained model artifacts & outputs
├── Preprocessing/            # Data cleaning & transformation scripts
├── Datasets/                 # Raw and processed datasets
├── Train/                    # Model training scripts
├── .gitignore
└── requirements.txt
```

---

## ⚙️ Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-username/supplynet360.git
cd supplynet360
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

**Train the model**
```bash
python Train/train.py
```

**Start the FastAPI inference server**
```bash
uvicorn Deploy.app:app --reload
# API available at http://127.0.0.1:8000
```

**Launch the Streamlit dashboard**
```bash
streamlit run app.py
```

---

## 📈 Results

- Successfully generated multi-step demand forecasts
- Enabled real-time prediction via REST API
- Visualized forecast trends with confidence intervals

---

## 🚧 Future Improvements

- [ ] Redis caching for faster inference
- [ ] Real-time data streaming with Apache Kafka
- [ ] Deep learning models (LSTM, Transformer)
- [ ] Docker + AWS deployment
- [ ] Automated model retraining pipelines

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---
