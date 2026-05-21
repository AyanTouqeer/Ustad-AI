#!/bin/bash

# 1. Start the FastAPI backend in the background on port 8000
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# 2. Start the Streamlit frontend on the dynamic port Google Cloud Run assigns
python -m streamlit run frontend.py --server.port $PORT --server.address 0.0.0.0