import os
from datetime import datetime
import socket

class SimpleLogger:
    def __init__(self, logfile="audit.log"):
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)
        self.logfile = os.path.join(self.log_dir, logfile)

    def log(self, message):
        hostname = socket.gethostname()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = "[{}] [{}] {}\n".format(timestamp, hostname, message)
        with open(self.logfile, "a", encoding="utf-8") as f:
            f.write(line)
