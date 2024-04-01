#!/bin/sh
uvicorn app:app --host 0.0.0.0 --port 80 &
streamlit run st_app.py --server.port=4444
#0.0.0.0:4444 -стримлит
#0.0.0.0:80 - fastapi