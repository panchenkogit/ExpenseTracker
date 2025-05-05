import subprocess

subprocess.Popen(["redis-server", "common_utils/redis/redis.conf"])

subprocess.Popen(
    [
        "uvicorn",
        "user_service.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
        "--reload",
    ]
)

subprocess.Popen(
    [
        "uvicorn",
        "subscriber_service.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8001",
        "--reload",
    ]
)

subprocess.Popen(
    [
        "uvicorn",
        "notification_service.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8002",
        "--reload",
    ]
)
