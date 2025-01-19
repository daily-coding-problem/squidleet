import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LogLevel:
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


# Log level hierarchy for comparison
LOG_LEVEL_PRIORITY = {
    LogLevel.DEBUG: 1,
    LogLevel.INFO: 2,
    LogLevel.WARN: 3,
    LogLevel.ERROR: 4,
}


def log(message: str, level: str = LogLevel.INFO):
    # Get the configured logging level or default to INFO if not set
    configured_level = os.getenv("LOGGING_LEVEL", LogLevel.INFO)
    show_detailed_logs = os.getenv("SHOW_DETAILED_LOGS", "False").lower() == "true"

    # Only log messages with a sufficient level
    if LOG_LEVEL_PRIORITY.get(level, 0) >= LOG_LEVEL_PRIORITY.get(configured_level, 0):
        if show_detailed_logs:
            timestamp = datetime.datetime.now().isoformat()
            if level == LogLevel.DEBUG:
                print(f"🐞 [{timestamp}] [{level}] {message}")
            elif level == LogLevel.INFO:
                print(f"ℹ️ [{timestamp}] [{level}] {message}")
            elif level == LogLevel.WARN:
                print(f"⚠️ [{timestamp}] [{level}] {message}")
            elif level == LogLevel.ERROR:
                print(f"❌ [{timestamp}] [{level}] {message}")

            return

        # Log message without timestamp or level
        print(message)
