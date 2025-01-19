import os
from utils.logger import log, LogLevel

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def initialize(cli_options: dict):
    leetcode_session = cli_options.get("leetcode_session") or os.getenv(
        "LEETCODE_SESSION"
    )
    if not leetcode_session:
        log("Using unauthenticated session", LogLevel.WARN)
        return

    os.environ["LEETCODE_SESSION"] = leetcode_session
    log("Using authenticated session", LogLevel.DEBUG)
