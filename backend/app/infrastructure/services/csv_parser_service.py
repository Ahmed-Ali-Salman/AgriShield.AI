"""
Infrastructure Service: CSV Parser.

Concrete implementation of FileParserService for CSV files.
"""

from typing import Dict, Any, List

from app.application.interfaces.file_parser_service import FileParserService


class CSVParserService(FileParserService):
    """Parses CSV and Excel files into structured data."""

    async def parse(self, file_path: str) -> List[Dict[str, Any]]:
        import pandas as pd  # Lazy import — only loaded when parsing

        ext = file_path.rsplit(".", 1)[-1].lower()
        if ext == "csv":
            df = pd.read_csv(file_path)
        elif ext in ("xls", "xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported: .{ext}")
        return df.to_dict(orient="records")

    def supported_extensions(self) -> List[str]:
        return ["csv", "xls", "xlsx"]
