import datetime

class LogLevel:
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"

def log(message: str, level: str = LogLevel.INFO):
    timestamp = datetime.datetime.now().isoformat()
    if level == LogLevel.INFO:
        print(f"ℹ️ [{timestamp}] [{level}] {message}")
    elif level == LogLevel.WARN:
        print(f"⚠️ [{timestamp}] [{level}] {message}")
    elif level == LogLevel.ERROR:
        print(f"❌ [{timestamp}] [{level}] {message}")
