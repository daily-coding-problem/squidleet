import argparse


def parse():
    parser = argparse.ArgumentParser(description="🦑 SquidLeet CLI Tool")
    parser.add_argument("--leetcode-session", type=str, help="LeetCode session token")
    parser.add_argument(
        "--practice-mode",
        type=str,
        choices=["custom", "random", "study-plan", "daily"],
        default="random",
        help="Practice mode",
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

    return vars(parser.parse_args())
