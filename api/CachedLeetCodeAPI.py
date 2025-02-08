import json
import hashlib
import tempfile
from typing import Any, Callable, Optional, List
from pathlib import Path
import time

from api.LeetCodeAPI import LeetCodeAPI
from utils.logger import log, LogLevel


def _get_cache_key(unique_id: str) -> str:
    """
    Generate a cache key based on a unique identifier (e.g., query or API parameters).
    :param unique_id: Unique identifier for the API request (e.g., slug, query, variable JSON).
    :return: Cache filename based on the MD5 hash of the unique ID.
    """
    return hashlib.md5(unique_id.encode("utf-8")).hexdigest()


class CachedLeetCodeAPI:
    def __init__(self, cache_dir: Optional[str] = None, cache_expiry: int = 3600):
        """
        Initialize the CachedLeetCodeAPI with caching functionality.
        :param cache_dir: Directory to store cached API results. Defaults to OS temp directory if None.
        :param cache_expiry: Expiry time for cache in seconds (default: 1 hour).
        """
        # Use the system's temporary directory if no cache directory is provided
        self.cache_dir = (
            Path(cache_dir or tempfile.gettempdir()) / "cached_leetcode_api"
        )
        self.cache_expiry = cache_expiry  # Expiry time in seconds
        self.cache_dir.mkdir(
            parents=True, exist_ok=True
        )  # Create cache directory if it doesn't exist

        self.api = (
            LeetCodeAPI()
        )  # Delegate actual API calls to existing LeetCodeAPI class

    def _read_from_cache(self, cache_key: str) -> Any:
        """
        Read data from cache if it exists and is valid.
        :param cache_key: Key corresponding to the cached data.
        :return: Cached data, or None if cache is invalid or missing.
        """
        cache_file = self.cache_dir / cache_key
        if cache_file.exists():
            # Check expiry
            if time.time() - cache_file.stat().st_mtime <= self.cache_expiry:
                with open(cache_file, "r") as f:
                    return json.load(f)

        return None  # Cache miss or expired

    def _write_to_cache(self, cache_key: str, data: Any) -> None:
        """
        Write data to cache.
        :param cache_key: Key corresponding to the cached data.
        :param data: Data to cache.
        """
        cache_file = self.cache_dir / cache_key
        with open(cache_file, "w") as f:
            json.dump(data, f)

    def _fetch_with_cache(
        self, fetch_func: Callable, unique_id: str, *args, **kwargs
    ) -> Any:
        """
        Fetch data with caching.
        :param fetch_func: Function to fetch data if cache is not available.
        :param unique_id: Unique identifier for the request (e.g., API parameters).
        :param args: Positional arguments to pass to the fetch function.
        :param kwargs: Keyword arguments to pass to the fetch function.
        :return: Fetched or cached data.
        """
        cache_key = _get_cache_key(unique_id)

        # Check cache first
        cached_data = self._read_from_cache(cache_key)
        if cached_data is not None:
            log(f"✅ Cache hit for {unique_id}", LogLevel.DEBUG)
            return cached_data

        # Cache miss, call the API
        log(f"❌ Cache miss for {unique_id}. Fetching from API...", LogLevel.DEBUG)
        api_data = fetch_func(*args, **kwargs)

        # Save API data to cache
        self._write_to_cache(cache_key, api_data)
        return api_data

    # Cached versions of API methods
    def fetch_problems(self, *args, **kwargs):
        """
        Cached version of fetch_problems
        """
        unique_id = f"fetch_problems-{json.dumps([args, kwargs], sort_keys=True)}"  # Unique key based on args
        return self._fetch_with_cache(
            self.api.fetch_problems, unique_id, *args, **kwargs
        )

    def fetch_daily_challenge(self, *args, **kwargs):
        """
        Cached version of fetch_daily_challenge
        """
        return self._fetch_with_cache(
            self.api.fetch_daily_challenge, "fetch_daily_challenge", *args, **kwargs
        )

    def fetch_problem(self, problem_slug: str, *args, **kwargs):
        """
        Cached version of fetch_problem
        """
        unique_id = f"fetch_problem-{problem_slug}"
        return self._fetch_with_cache(
            self.api.fetch_problem, unique_id, problem_slug, *args, **kwargs
        )

    def get_study_plan(self, slug: str, *args, **kwargs):
        """
        Cached version of get_study_plan
        """
        unique_id = f"get_study_plan-{slug}"
        return self._fetch_with_cache(
            self.api.get_study_plan, unique_id, slug, *args, **kwargs
        )

    def fetch_company_questions(self, company_slug: str, *args, **kwargs):
        """
        Cached version of fetch_company_questions
        """
        unique_id = f"fetch_company_questions-{company_slug}"
        return self._fetch_with_cache(
            self.api.fetch_company_questions, unique_id, company_slug, *args, **kwargs
        )

    def fetch_company_questions_for_duration(
        self,
        company_name: str,
        duration: str,
        difficulties: Optional[List[str]] = None,
        tags: Optional[list] = None,
        *args,
        **kwargs,
    ):
        """
        Wrapper around `fetch_company_questions` that accepts a company name,
        duration, and an optional difficulty filter to fetch questions for a specific time range.

        This method is cached to avoid redundant API calls.

        :param company_name: Name of the company (e.g., 'amazon', 'google').
        :param duration: Duration to filter questions (e.g., 'thirty-days', 'three-months').
                         Valid durations:
                         - "thirty-days"
                         - "three-months"
                         - "six-months"
                         - "more-than-six-months"
                         - "all"
        :param difficulties: (Optional) Difficulty filter to narrow down the results.
                           Valid options: "EASY", "MEDIUM", "HARD".
        :param tags: (Optional) List of topic tags to filter the questions.
        :return: A dictionary containing the questions and metadata.
        """

        # Validate duration input
        valid_durations = [
            "thirty-days",
            "three-months",
            "six-months",
            "more-than-six-months",
            "all",
        ]
        if duration not in valid_durations:
            raise ValueError(
                f"Invalid duration: {duration}. Must be one of {valid_durations}."
            )

        # Validate difficulty input
        valid_difficulties = ["EASY", "MEDIUM", "HARD"]
        difficulty_filter = None
        if difficulties:
            if difficulties not in valid_difficulties:
                raise ValueError(
                    f"Invalid difficulty: {difficulties}. Must be one of {valid_difficulties}."
                )

            # Create a difficulty filter with the operator "IS"
            difficulty_filter = {"difficulties": difficulties, "operator": "IS"}

        # Validate tags input
        topic_filter = None
        if tags:
            topic_tags = self.api.get_topic_tags()
            valid_tags = [tag.lower() for tag in topic_tags]
            standardized_tags = [tag.lower() for tag in tags]
            if any(tag not in valid_tags for tag in standardized_tags):
                raise ValueError(
                    f"Invalid tags. Supported tags: {', '.join(valid_tags)}"
                )

            # Create a topic filter with the operator "IS"
            topic_filter = {
                "tags": standardized_tags,
                "operator": "IS",
            }

        # Construct the favorite_slug based on company name and duration
        favorite_slug = f"{company_name.lower()}-{duration}"

        # Append difficulties to the unique id if provided
        unique_id = (
            f"{favorite_slug}-{'-'.join(difficulties)}"
            if difficulties
            else favorite_slug
        )

        results = self._fetch_with_cache(
            self.api.fetch_company_questions,
            unique_id,
            favorite_slug,
            difficulty_filter,
            topic_filter,
            *args,
            **kwargs,
        )

        # Navigate to the questions in the actual response structure
        favorite_question_list = results.get("data", {}).get("favoriteQuestionList", {})
        return favorite_question_list.get("questions", [])
