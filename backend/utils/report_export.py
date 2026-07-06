"""
Report Export Utilities
"""

from pathlib import Path


class ReportExporter:

    @staticmethod
    def export_markdown(
        report: str,
        filename: str
    ):

        output_dir = Path("reports")

        output_dir.mkdir(
            exist_ok=True
        )

        path = output_dir / f"{filename}.md"

        path.write_text(
            report,
            encoding="utf-8"
        )

        return path