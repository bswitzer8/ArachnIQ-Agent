import requests
import json
import time
from typing import Dict, Any, List

class TestRunner:
    """
    Executes test cases against a target API.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.results = []

    def run_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a single test case.
        """
        name = test_case.get("name")
        method = test_case.get("method", "GET").upper()
        path = test_case.get("path")
        body = test_case.get("body")
        expected_status = test_case.get("expected_status")

        if not path.startswith("/"):
            path = "/" + path

        url = f"{self.base_url}{path}"

        result = {
            "name": name,
            "method": method,
            "path": path,
            "expected_status": expected_status,
            "passed": False,
            "status": "Running",
            "message": "",
            "response_snippet": ""
        }

        try:
            start_time = time.time()
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                response = requests.post(url, json=body, timeout=5)
            elif method == "DELETE":
                response = requests.delete(url, timeout=5)
            elif method == "PUT":
                response = requests.put(url, json=body, timeout=5)
            else:
                result["status"] = "Error"
                result["message"] = f"Unsupported method: {method}"
                return result

            duration = time.time() - start_time

            result["actual_status"] = response.status_code
            result["duration"] = f"{duration:.3f}s"
            result["response_snippet"] = response.text[:200]

            if response.status_code == expected_status:
                result["passed"] = True
                result["status"] = "PASS"
                result["message"] = "Status code matched expectation."
            else:
                result["passed"] = False
                result["status"] = "FAIL"
                result["message"] = f"Expected {expected_status}, got {response.status_code}."

        except Exception as e:
            result["status"] = "Error"
            result["message"] = f"Request failed: {str(e)}"
            result["passed"] = False

        return result

    def run_suite(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Runs a full suite of test cases.
        """
        self.results = []
        for test in test_cases:
            result = self.run_test(test)
            self.results.append(result)
        return self.results
