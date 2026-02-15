"""
Infrastructure: External CVE API Client.

Fetches known vulnerability data for supplier IT security assessment.
"""

from typing import Dict, Any, List, Optional

import httpx

from app.config import settings


class CVEClient:
    """Client for the NIST National Vulnerability Database API."""

    def __init__(self):
        self._base_url = settings.CVE_API_BASE_URL

    async def search_vulnerabilities(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for CVEs related to a keyword (e.g., supplier's software stack).

        Returns a simplified list of vulnerability records.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self._base_url,
                    params={"keywordSearch": keyword, "resultsPerPage": limit},
                    timeout=30.0,
                )
                response.raise_for_status()
                data = response.json()
                return data.get("vulnerabilities", [])
            except httpx.HTTPError:
                return []
