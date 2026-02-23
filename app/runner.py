import requests
import json
import os
from datetime import datetime

class TestRunner:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = []

    def run_test(self, test_case):
        name = test_case.get("name")
        method = test_case.get("method", "GET")
        path = test_case.get("path")
        body = test_case.get("body")
        expected_status = test_case.get("expected_status")
        
        url = f"{self.base_url}{path}"
        
        try:
            start_time = datetime.now()
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                response = requests.post(url, json=body, timeout=5)
            else:
                return {"name": name, "status": "Error", "message": f"Unsupported method: {method}"}
            
            duration = (datetime.now() - start_time).total_seconds()
            
            passed = response.status_code == expected_status
            
            result = {
                "name": name,
                "method": method,
                "path": path,
                "actual_status": response.status_code,
                "expected_status": expected_status,
                "passed": passed,
                "response": response.text[:200], # Truncate long responses
                "duration": f"{duration:.3f}s"
            }
            
            if not passed:
                result["message"] = f"Expected {expected_status}, got {response.status_code}"
            else:
                result["message"] = "Success"
                
            return result
            
        except Exception as e:
            return {
                "name": name,
                "method": method,
                "path": path,
                "passed": False,
                "status": "Error",
                "message": str(e)
            }

    def run_suite(self, test_cases, callback=None):
        self.results = []
        for test in test_cases:
            result = self.run_test(test)
            self.results.append(result)
            if callback:
                callback(result)
        return self.results

    def generate_reports(self, output_dir="reports"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON Report
        json_path = os.path.join(output_dir, f"report_{timestamp}.json")
        with open(json_path, "w") as f:
            json.dump(self.results, f, indent=2)
            
        # Markdown Report
        md_path = os.path.join(output_dir, f"report_{timestamp}.md")
        with open(md_path, "w") as f:
            f.write(f"# ArachnIQ-Agent Test Report
")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

")
            f.write("| Test Name | Method | Path | Expected | Actual | Status | Message |
")
            f.write("| --- | --- | --- | --- | --- | --- | --- |
")
            for r in self.results:
                status = "✅ PASS" if r.get("passed") else "❌ FAIL"
                f.write(f"| {r['name']} | {r.get('method')} | {r.get('path')} | {r.get('expected_status')} | {r.get('actual_status')} | {status} | {r.get('message')} |
")
        
        return json_path, md_path
