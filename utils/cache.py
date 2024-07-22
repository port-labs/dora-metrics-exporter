"""
[Singleton Pattern] - Only one InMemory Cache can be instantiated
"""

import asyncio
from typing import Dict, Any

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class InMemoryCache(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}
        self.lock = asyncio.Lock()

    async def upsert(self, key, data):
        """
        Sets or updates a cache entry with the given key.

        Parameters:
        - key (str): The key to use for the cache entry.
        - data (dict): The data to be cached.
        """
        async with self.lock:
            if key in self.cache:
                self.cache[key].update(data)
            else:
                self.cache[key] = data
            return True

    async def get(self, key) -> Dict[str, Any]:
        """
        Retrieves cached data using the given key.

        Parameters:
        - key (str): The key to retrieve from the cache.

        Returns:
        - dict: The cached data associated with the key, or None if not found.
        """
        async with self.lock:
            return self.cache.get(key, {})

    async def delete(self, key):
        """
        Deletes cached data associated with the given key.

        Parameters:
        - key (str): The key to delete from the cache.

        Returns:
        - bool: True if deletion was successful, False otherwise (key not found).
        """
        async with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False

class CACHE_KEYS:
    WORKFLOWS_CACHE_KEY:str = "__CICD_CACHE_KEY"
    SERVICE_CACHE_KEY:str = "__SOURCE_CONTROL_SERVICES_CACHE_KEY"
    INCIDENTS_CACHE_KEY:str = "__INCIDENT_CACHE_KEY"
    
