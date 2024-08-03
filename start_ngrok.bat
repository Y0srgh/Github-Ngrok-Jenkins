@echo off
REM Start ngrok on port 8080
start ngrok http 8080

REM Wait for ngrok to initialize
timeout /t 10

REM Run the Python script to update GitHub webhook
python update_github_webhook.py
