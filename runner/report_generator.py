import json
import os
from datetime import datetime
from typing import List, Dict, Any

class ReportGenerator:
    """
    Generates JSON and Markdown reports from test results.
    """
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_json_report(self, results: List[Dict[str, Any]]) -> str:
        """
        Generates a JSON report file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)

        return filepath

    def generate_markdown_report(self, results: List[Dict[str, Any]]) -> str:
        """
        Generates a Markdown report file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)

        passed_count = sum(1 for r in results if r.get("passed"))
        failed_count = len(results) - passed_count

        with open(filepath, "w") as f:
            f.write(f"# ArachnIQ-Agent Test Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Summary:**\n")
            f.write(f"- Total Tests: {len(results)}\n")
            f.write(f"- Passed: {passed_count} ✅\n")
            f.write(f"- Failed: {failed_count} ❌\n\n")

            f.write("| Test Name | Method | Path | Expected | Actual | Status | Message |\n")
            f.write("| --- | --- | --- | --- | --- | --- | --- |\n")

            for r in results:
                status_icon = "✅" if r.get("passed") else "❌"
                # Handle missing 'actual_status' in case of request error
                actual = r.get("actual_status", "N/A")

                # Escape pipe characters in message to avoid breaking table
                message = str(r.get("message", "")).replace("|", "\\|")

                f.write(f"| {r['name']} | {r.get('method')} | {r.get('path')} | {r.get('expected_status')} | {actual} | {status_icon} | {message} |\n")

        return filepath
