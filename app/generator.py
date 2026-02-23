import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

class TestGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def generate_tests(self, api_schema: str):
        prompt = f"""
        You are an expert QA Automation Engineer. 
        Your task is to generate comprehensive test cases for the following FastAPI application.
        
        API Schema/Endpoints:
        {api_schema}
        
        Requirements:
        1. Generate test cases covering:
           - Happy path scenarios.
           - Edge cases (negative numbers, empty strings, extremely large values).
           - Security/Validation (missing fields).
           - Specific logic bugs mentioned in the API description.
        
        2. Format your response ONLY as a JSON list of objects.
        Each object must have:
        - name: A descriptive name for the test.
        - method: HTTP method (GET, POST, etc.)
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
        
        Ensure the JSON is valid and ready to be parsed.
        """
        
        response = self.model.generate_content(prompt)
        
        # Clean the response if it contains markdown code blocks
        text = response.text.strip()
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

if __name__ == "__main__":
    # Quick local test
    schema = """
    - GET /: Root endpoint
    - POST /users/register: {username, email}
    - GET /products: List all products
    - GET /products/{product_id}: Get product details. Bug: crashes on id 999.
    - POST /cart/add: {product_id, quantity}. Bug: allows negative quantity.
    - POST /checkout: Process cart. Bug: fails if more than 5 items.
    """
    generator = TestGenerator()
    tests = generator.generate_tests(schema)
    print(json.dumps(tests, indent=2))
