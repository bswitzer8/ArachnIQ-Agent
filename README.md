# ArachnIQ-Agent 🕷️🤖

**ArachnIQ-Agent** is a lean, AI-powered API testing showcase built for the Google Hackathon. It demonstrates how Google Gemini can be used to autonomously explore an API, generate intelligent test cases (including edge cases and negative scenarios), and execute them in a real-time dashboard.

## 🚀 Key Features

- **AI-Driven Test Generation**: Uses `gemini-1.5-pro` to analyze API schemas and generate high-coverage test suites.
- **Automated Bug Discovery**: Successfully identifies intentional logic bugs and edge cases in the target API.
- **Real-time CLI Dashboard**: A beautiful, live-updating terminal interface powered by `Rich`.
- **Comprehensive Reporting**: Automatically generates detailed Markdown and JSON reports for every test run.
- **Mock API Included**: Comes with a built-in FastAPI service with pre-defined "bugs" for immediate demonstration.

## 🛠️ Quick Start

### 1. Prerequisites
- Python 3.9+
- A Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/ArachnIQ-Agent.git
cd ArachnIQ-Agent

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Copy the `.env.template` to `.env` and add your Gemini API key:
```bash
cp .env.template .env
# Edit .env and set GEMINI_API_KEY=your_key_here
```

### 4. Run the Demo
```bash
python -m app.main
```

## 🧠 How it Works

1. **Schema Analysis**: The system feeds the API endpoint definitions to Google Gemini.
2. **Intelligence Phase**: Gemini identifies potential weaknesses (e.g., "What happens if I add a negative quantity to the cart?") and generates a JSON-structured test suite.
3. **Execution**: The test runner executes the HTTP requests against the local FastAPI mock server.
4. **Validation**: Responses are validated against the AI's expected results.
5. **Visualization**: Results are streamed to a live CLI dashboard.

## 📁 Repository Structure
- `app/mock_api.py`: A FastAPI application with intentional logic bugs.
- `app/generator.py`: The Gemini-powered test generation engine.
- `app/runner.py`: Executes tests and generates reports.
- `app/main.py`: The orchestration layer and CLI dashboard.
- `reports/`: Directory where test results are saved.

---
Built with 🕷️ by the ArachnIQ Team for the Google Hackathon.
