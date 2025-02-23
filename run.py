import subprocess

subprocess.Popen(["uvicorn", "user_service.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"])

subprocess.Popen(["uvicorn", "subscriber_servise.main:app", "--host", "127.0.0.1", "--port", "8001", "--reload"])
