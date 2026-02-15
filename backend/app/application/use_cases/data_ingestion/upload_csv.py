"""
Use Case: Upload CSV.

Handles ingestion of supplier data from uploaded CSV files.
"""

from typing import Dict, Any, List

from app.application.interfaces.file_parser_service import FileParserService


class UploadCSVUseCase:
    """Parse and validate an uploaded CSV file for data ingestion."""

    def __init__(self, parser: FileParserService):
        self._parser = parser

    async def execute(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse the uploaded file and return structured data.

        Raises:
            ValueError: If the file format is not supported.
        """
        extension = file_path.rsplit(".", 1)[-1].lower()
        if extension not in self._parser.supported_extensions():
            raise ValueError(
                f"Unsupported file format: .{extension}. "
                f"Supported: {self._parser.supported_extensions()}"
            )

        return await self._parser.parse(file_path)
