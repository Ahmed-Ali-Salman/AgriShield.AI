"""
Application Interface: FileParserService.

Abstract interface for parsing uploaded data files (CSV, Excel).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class FileParserService(ABC):
    """Abstract file parsing service."""

    @abstractmethod
    async def parse(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse a data file and return a list of row dictionaries."""
        ...

    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """Return list of supported file extensions."""
        ...
