import json
import hashlib
import tempfile
from typing import Any, Callable, Optional
from pathlib import Path
import time

from api.LeetCodeAPI import LeetCodeAPI
from utils.logger import log, LogLevel


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

    def _get_cache_key(self, unique_id: str) -> str:
        """
        Generate a cache key based on a unique identifier (e.g., query or API parameters).
        :param unique_id: Unique identifier for the API request (e.g., slug, query, variable JSON).
        :return: Cache filename based on the MD5 hash of the unique ID.
        """
        return hashlib.md5(unique_id.encode("utf-8")).hexdigest()

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
        cache_key = self._get_cache_key(unique_id)

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
            self.api.fetch_daily_challenge, "fetch_daily_challenge"
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
