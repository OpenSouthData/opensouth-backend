# gunicorn_config.py
import os

port = os.getenv("PORT") 


bind = f"0.0.0.0:{port}"  # Specify the host and port
workers = 4  # Number of worker processes
timeout = 60*10 # Time in seconds before a worker is killed and restarted
