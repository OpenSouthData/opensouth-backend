# gunicorn_config.py

bind = "0.0.0.0:8000"  # Host and port to bind to
workers = 4  # Adjust based on the number of CPU cores available
worker_class = 'gevent'  # or 'uvicorn.workers.UvicornWorker'
timeout = 60  # Worker timeout (in seconds)
keepalive = 2  # Keep-alive duration (in seconds)

# Optional: Log configuration
accesslog = '-'  # Access log to stdout
errorlog = '-'  # Error log to stdout
loglevel = 'info'  # Log level

# Optional: Maximum number of simultaneous clients
worker_connections = 1000  # Number of simultaneous clients per worker

# Optional: Preload the application code before forking worker processes
preload_app = True  # Preload the application code (saves memory)
