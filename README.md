# ArachnIQ-Agent 🕷️🤖

**ArachnIQ-Agent** is a hackathon-ready showcase of autonomous AI-powered API testing. This project demonstrates how Large Language Models (LLMs) like Google Gemini can be leveraged to intelligently explore an API, generate test cases (including edge cases and security validation), and execute them in real-time.

## 🚀 Demo Highlights

- **Self-Contained Environment**: Includes a "vulnerable" Mock API with intentional bugs for the AI to find.
- **AI Test Generation**: Uses Google Gemini to analyze the API schema and dream up test scenarios.
- **Live Dashboard**: Features a beautiful CLI dashboard using `Rich` to show tests running in real-time.
- **Automated Reporting**: Generates JSON and Markdown execution reports.

## 📂 Project Structure

```
ArachnIQ-Agent/
├── api/            # FastAPI application with intentional bugs
├── tests/          # AI Test Generator (Gemini integration)
├── runner/         # Test Runner & Report Generator
├── dashboard/      # CLI Dashboard entry point
├── reports/        # Output directory for test reports
└── requirements.txt
```

## 🛠️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ArachnIQ-Agent.git
    cd ArachnIQ-Agent
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key:**
    Copy `.env.template` to `.env` and add your Google Gemini API key.
    ```bash
    cp .env.template .env
    # Edit .env and set GEMINI_API_KEY=your_key_here
    ```
    > **Note:** If you don't have a key, the system will automatically fall back to "Mock Mode" using pre-defined test cases.

## ▶️ Running the Demo

To start the full demo (API + Test Generation + Dashboard):

```bash
python -m dashboard.cli_dashboard
```

### What to expect:
1.  The **Mock API** will start in the background.
2.  The **AI Generator** will analyze the API and create a test suite.
3.  The **Live Dashboard** will appear, showing each test execution.
4.  **Bugs Found!** You will see some tests FAIL. This is intentional! The AI has successfully found the bugs hidden in the Mock API.
5.  **Reports** will be saved to the `reports/` directory.

## 🐛 Intentional Bugs to Look For

The Mock API contains several "traps" for the AI to find:
- **User Registration**: Allows duplicate users (Logic Error).
- **Product Details**: ID `999` crashes the server (500 Internal Server Error).
- **Cart**: Allows adding negative quantities (Validation Missing).
- **Checkout**: "Fails" if more than 5 items are in the cart.

## 📊 Reports

After execution, check the `reports/` folder for:
- `report_YYYYMMDD_HHMMSS.md`: A readable summary of the test run.
- `report_YYYYMMDD_HHMMSS.json`: Raw test data.

---
*Built for the Google Hackathon.*
