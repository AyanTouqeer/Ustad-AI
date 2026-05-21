# Ustad.ai 

> **An AI-Driven Marketplace Formalizing the Informal Service Economy.**
> Developed by Team infinityARC Studios.

![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Google Cloud Run](https://img.shields.io/badge/Google_Cloud_Run-4285F4?style=flat&logo=google-cloud&logoColor=white)
![Firestore](https://img.shields.io/badge/Firestore-FFCA28?style=flat&logo=firebase&logoColor=black)

---

## 📖 Project Overview

**The Problem:** The informal service economy (plumbers, electricians, mechanics) operates on inefficient word-of-mouth networks. Customers struggle to find verified help during emergencies, and skilled providers lose out on high-intent leads due to a lack of digital presence.

**The Solution:** Ustad.ai is a dual-sided, intelligent routing platform. By leveraging an Agentic AI orchestrator, the platform allows customers to describe their problem in natural language (e.g., *"Pipe burst in Chungi No. 22!"*). The AI extracts the intent, urgency, and location, autonomously routing a highly qualified lead directly to the dashboard of the nearest relevant service provider.

---

## ✨ Core Features

* 🧠 **Agentic AI Orchestration:** Processes unstructured natural language requests to classify job types and extract actionable location data.
* 🔄 **Dual-Portal System:** Separate, optimized interfaces for Customers (request generation) and Providers (lead management).
* ⚡ **Real-Time Data Sync:** Powered by Google Cloud Firestore for immediate lead dispatch.
* 📱 **Cloud-Native & Responsive:** Deployed as a unified Docker container on Google Cloud Run, ensuring mobile responsiveness and high availability.

---

## 🏗️ System Architecture

Ustad.ai is engineered using a robust, decoupled microservice architecture, containerized for seamless cloud deployment.

* **Frontend (UI):** `Streamlit` - Provides a rapid, stateful, and highly responsive user interface for both portals.
* **Backend (API):** `FastAPI` / `Uvicorn` - A high-performance RESTful orchestrator that handles AI routing logic and secure database transactions.
* **Database:** `Google Cloud Firestore` - A NoSQL document database managing real-time state for users, providers, and active leads.
* **Deployment Infrastructure:** `Docker` & `Google Cloud Run` (Serverless container deployment).

---

## 🚀 Agentic AI Workflow: Antigravity & Gemini CLI

Our development journey was a testament to agile adaptation and leveraging the right AI tools at the right time. 

**Initial Phases (Antigravity):**
This project began by heavily utilizing **Antigravity** to accelerate development, enforce architectural best practices, and "vibe code" our core logic. During this phase, we used Antigravity to:
1. **FastAPI Routing Logic:** Generate the foundational asynchronous endpoints for intent extraction.
2. **UI Prototyping:** Rapidly iterate on the Streamlit Customer and Provider dashboards using natural language layout requests.

**The Pivot (VS Code & Gemini CLI):**
Mid-hackathon, a sudden platform update to the Antigravity IDE introduced workflow friction and navigation confusion. To maintain momentum and hit our deployment deadline, our team executed a rapid pivot. We transitioned our environment to **VS Code** for precise local development. For our complex cloud deployment, we leveraged the **Gemini CLI available natively in the Google Cloud Shell terminal** to successfully write our unified `Dockerfile` and `start.sh` scripts, bridging the Streamlit and FastAPI services into a single deployable Cloud Run container.

*(Note: Full generation logs and task traces from the Antigravity workspace are included in the official hackathon submission zip file).*

---

## 🌍 Live Demo & Links

* **Live Web App:** https://ustad-ai-750612016119.asia-south2.run.app 
* **Pitch & Demo Video:** https://drive.google.com/file/d/1T_D8hnhFGUI5XAxmZMDTO27-TiN-tkg0/view?usp=sharing 

---

## 💻 Local Installation (Quick Start)

To run the Ustad.ai microservices locally on your machine, first ensure your `gcp-key.json` database credential is placed in the root directory (Note: This file is strictly excluded via `.gitignore` for security). 

Then, execute the following commands in your terminal:

```bash
# 1. Clone the repository and navigate into it
git clone [https://github.com/AyanTouqeer/Ustad-AI.git](https://github.com/AyanTouqeer/Ustad-AI.git)
cd Ustad-AI

# 2. Install required Python dependencies
pip install -r requirements.txt

# 3. Make the startup script executable and launch the unified server
chmod +x start.sh
./start.sh
