import argparse


def parse():
    parser = argparse.ArgumentParser(description="🦑 SquidLeet CLI Tool")
    parser.add_argument("--leetcode-session", type=str, help="LeetCode session token")
    parser.add_argument(
        "--practice-mode",
        type=str,
        choices=["custom", "random", "study-plan", "daily"],
        help="Practice mode",
        default="random",
    )
    parser.add_argument(
        "--difficulties",
        type=str,
        help="Comma-separated difficulty levels (easy, medium, hard)",
        default="easy,medium,hard",
    )
    parser.add_argument(
        "--problems",
        type=str,
        help="Comma-separated problem slugs (e.g., 'two-sum,fizz-buzz')",
        default="two-sum",
    )
    parser.add_argument(
        "--plan-name",
        type=str,
        help="Study plan slug (e.g., 'top-interview-150' or 'leetcode-75')",
        default="top-interview-150",
    )
    parser.add_argument(
        "--language", type=str, help="Programming language to use", default="python"
    )
    parser.add_argument(
        "--time-limit", type=int, help="Time limit for practice in minutes", default=45
    )
    parser.add_argument(
        "--editor", type=str, help="Editor to use for files", default="default"
    )
    parser.add_argument(
        "--open-in-browser", action="store_true", help="Open the problem in a browser"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARN", "ERROR"],
        help="Log level",
        default="INFO",
    )
    parser.add_argument(
        "--show-detailed-logs",
        action="store_true",
        help="Show timestamp and log level in logs",
        default=False,
    )

    return vars(parser.parse_args())
