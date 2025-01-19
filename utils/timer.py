import time

expiration_time = 0

def start_timer(time_limit: int, problem_slug: str):
    """
    Start a timer for the specified time limit.
    :param time_limit: Time limit in seconds.
    :param problem_slug: Slug of the problem.
    """
    global expiration_time
    expiration_time = time.time() + time_limit
    print(f"⏳ Timer started for problem: {problem_slug}")

def get_time_remaining() -> int:
    """
    Get the remaining time in seconds.
    :return: Remaining time in seconds.
    """
    remaining = int(expiration_time - time.time())
    return max(0, remaining)
