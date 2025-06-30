import requests
from typing import Any


class LuceneClient:
    def __init__(self, base_url: str = "http://localhost:4567"):
        self.base_url = base_url.rstrip("/")

    def search(self, query: str, top_k: int = 10) -> list[dict[str, Any]]:
        """
        Sends a query to the Lucene search engine and returns ranked results.
        
        Returns:
            List of dicts like: [{"documentId": "doc1", "score": 2.345}, ...]
        """
        endpoint = f"{self.base_url}/search"
        payload = {"query": query, "topK": top_k}

        try:
            response = requests.post(endpoint, json=payload, timeout=5)
            response.raise_for_status()
            results = response.json()
            return results
        except requests.RequestException as e:
            print(f"[LuceneClient] Request failed: {e}")
            return []
        except ValueError:
            print("[LuceneClient] Invalid JSON received")
            return []

    def ping(self) -> bool:
        """
        Optional health check (if your Java API supports it).
        """
        try:
            response = requests.get(f"{self.base_url}/ping")
            return response.status_code == 200
        except requests.RequestException:
            return False
