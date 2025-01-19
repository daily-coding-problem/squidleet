import os
from utils.logger import log, LogLevel

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def initialize(cli_options):
    leetcode_session = cli_options.get("leetcode_session") or os.getenv(
        "LEETCODE_SESSION"
    )
    if not leetcode_session:
        raise ValueError(
            "❌ Missing LEETCODE_SESSION. Provide it via CLI or as an environment variable."
        )

    os.environ["LEETCODE_SESSION"] = leetcode_session
    log("LeetCode session initialized successfully.", LogLevel.DEBUG)
