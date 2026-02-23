import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

class TestGenerator:
    """
    Generates API test cases using Google Gemini.
    """
    def __init__(self, mock_mode: bool = False):
        self.mock_mode = mock_mode
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key or self.api_key == "your_api_key_here":
            print("Warning: GEMINI_API_KEY not found or invalid. Switching to MOCK mode.")
            self.mock_mode = True

        if not self.mock_mode:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-pro')
            except Exception as e:
                print(f"Error configuring Gemini: {e}. Switching to MOCK mode.")
                self.mock_mode = True

    def generate_tests(self, api_schema: str) -> List[Dict[str, Any]]:
        """
        Generates test cases based on the provided API schema.
        """
        if self.mock_mode:
            return self._get_mock_tests()

        prompt = f"""
        You are an expert QA Automation Engineer.
        Your task is to generate comprehensive test cases for the following FastAPI application.

        API Schema/Endpoints:
        {api_schema}

        Requirements:
        1. Generate test cases covering:
           - Happy path scenarios (Success).
           - Edge cases (negative numbers, empty strings, extremely large values).
           - Security/Validation (missing fields).
           - Specific logic bugs hinted at in the descriptions.

        2. Format your response ONLY as a JSON list of objects.
        Each object must have:
        - name: A descriptive name for the test.
        - method: HTTP method (GET, POST, DELETE, etc.)
        - path: The API endpoint path.
        - body: (Optional) The JSON request body.
        - expected_status: The expected HTTP status code.
        - description: What this test is checking.

        Example Format:
        [
            {{
                "name": "Register User Success",
                "method": "POST",
                "path": "/users/register",
                "body": {{"username": "testuser", "email": "test@example.com"}},
                "expected_status": 200,
                "description": "Checks if a user can be registered with valid data."
            }}
        ]

        Ensure the JSON is valid and strictly follows the format.
        """

        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            print(f"Error generating content: {e}. Returning mock tests.")
            return self._get_mock_tests()

    def _parse_response(self, text: str) -> List[Dict[str, Any]]:
        """Parses the AI response, handling potential markdown formatting."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]

        try:
            return json.loads(text.strip())
        except json.JSONDecodeError as e:
            print(f"Failed to parse AI response as JSON: {e}")
            print(f"Raw response: {text}")
            return []

    def _get_mock_tests(self) -> List[Dict[str, Any]]:
        """Returns hardcoded test cases for demonstration/fallback purposes."""
        return [
            {
                "name": "Root Check",
                "method": "GET",
                "path": "/",
                "expected_status": 200,
                "description": "Verify API is online."
            },
            {
                "name": "Register User - Success",
                "method": "POST",
                "path": "/users/register",
                "body": {"username": "alice", "email": "alice@example.com"},
                "expected_status": 200,
                "description": "Register a valid user."
            },
            {
                "name": "Register User - Duplicate (Bug)",
                "method": "POST",
                "path": "/users/register",
                "body": {"username": "alice", "email": "alice@example.com"},
                "expected_status": 400,
                "description": "Should fail for duplicate user (Intentionally fails due to bug)."
            },
            {
                "name": "Get Product - Valid",
                "method": "GET",
                "path": "/products/1",
                "expected_status": 200,
                "description": "Get an existing product."
            },
            {
                "name": "Get Product - Crash ID (Bug)",
                "method": "GET",
                "path": "/products/999",
                "expected_status": 404,
                "description": "Should return 404, but API crashes (Intentionally fails due to bug)."
            },
            {
                "name": "Add to Cart - Valid",
                "method": "POST",
                "path": "/cart/add",
                "body": {"product_id": 1, "quantity": 1},
                "expected_status": 200,
                "description": "Add item to cart."
            },
            {
                "name": "Add to Cart - Negative Quantity (Bug)",
                "method": "POST",
                "path": "/cart/add",
                "body": {"product_id": 1, "quantity": -5},
                "expected_status": 400,
                "description": "Should fail for negative quantity (Intentionally passes due to bug)."
            },
             {
                "name": "Checkout - Success",
                "method": "POST",
                "path": "/cart/checkout",
                "expected_status": 200,
                "description": "Checkout successfully."
            }
        ]

if __name__ == "__main__":
    # Local test
    gen = TestGenerator(mock_mode=True)
    print(json.dumps(gen.generate_tests(""), indent=2))
