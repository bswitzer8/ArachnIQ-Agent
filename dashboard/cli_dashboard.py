import time
import threading
import uvicorn
import os
import sys
import argparse
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich import box
from rich.text import Text

# Add project root to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.dummy_api import app
from tests.generator import TestGenerator
from runner.test_runner import TestRunner
from runner.report_generator import ReportGenerator

console = Console()

def run_api():
    """Starts the FastAPI server in a separate thread."""
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="critical")

def main():
    parser = argparse.ArgumentParser(description="ArachnIQ-Agent CLI Dashboard")
    parser.add_argument("--mock", action="store_true", help="Force mock mode (no API calls to Gemini)")
    args = parser.parse_args()

    console.print(Panel("[bold cyan]ArachnIQ-Agent: AI-Powered API Testing Demo[/bold cyan]", box=box.DOUBLE))
    
    # 1. Start Mock API
    console.print("[yellow]🕷️ Starting ArachnIQ Mock API...[/yellow]")
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    time.sleep(2) # Give it a moment to start
    console.print("[green]✓ API Online at http://127.0.0.1:8000[/green]")
    
    # 2. Generate Tests
    console.print("[yellow]🧠 Analyzing API Schema and Generating Test Cases...[/yellow]")

    # This schema would ideally be introspected from FastAPI's openapi.json, but hardcoded here for the demo flow
    schema_summary = """
    Endpoints:
    - GET /: Welcome message.
    - POST /users/register: {username, email}. Bug: No duplicate check.
    - GET /products: List products.
    - GET /products/{product_id}: Details. Bug: Exception on ID 999.
    - POST /cart/add: {product_id, quantity}. Bug: Allows negative quantity.
    - POST /checkout: Process cart. Bug: Fails if > 5 items.
    """
    
    generator = TestGenerator(mock_mode=args.mock)
    test_cases = generator.generate_tests(schema_summary)

    if not test_cases:
        console.print("[bold red]Failed to generate test cases. Exiting.[/bold red]")
        return

    console.print(f"[green]✓ Successfully generated {len(test_cases)} test cases.[/green]")
    if generator.mock_mode:
        console.print("[dim](Running in MOCK mode - using pre-defined test cases)[/dim]")

    # 3. Run Tests with Live Dashboard
    console.print("\n[bold]🚀 Starting Test Execution...[/bold]\n")
    runner = TestRunner(base_url="http://127.0.0.1:8000")
    results = []
    
    table = Table(title="Live Test Execution", box=box.ROUNDED)
    table.add_column("Test Name", style="cyan")
    table.add_column("Method", style="magenta")
    table.add_column("Path", style="blue")
    table.add_column("Status", justify="center")
    table.add_column("Message", style="dim")

    with Live(table, refresh_per_second=4):
        for test in test_cases:
            result = runner.run_test(test)
            results.append(result)
            
            status_str = "[green]PASS[/green]" if result.get("passed") else "[red]FAIL[/red]"
            if result.get("status") == "Error":
                status_str = "[bold red]ERROR[/bold red]"
                
            table.add_row(
                result["name"],
                result.get("method", "GET"),
                result.get("path", "/"),
                status_str,
                result.get("message", "")
            )
            time.sleep(0.5) # For visual effect

    # 4. Final Summary
    passed_count = sum(1 for r in results if r.get("passed"))
    failed_count = len(results) - passed_count
    
    console.print("\n[bold]Test Summary:[/bold]")
    console.print(f"Total: {len(results)}")
    console.print(f"Passed: [green]{passed_count}[/green]")
    console.print(f"Failed: [red]{failed_count}[/red]")
    
    # 5. Generate Reports
    reporter = ReportGenerator()
    json_rep = reporter.generate_json_report(results)
    md_rep = reporter.generate_markdown_report(results)

    console.print("\n[bold blue]📝 Reports generated:[/bold blue]")
    console.print(f"- JSON: {json_rep}")
    console.print(f"- Markdown: {md_rep}")

    console.print("\n[bold cyan]ArachnIQ-Agent Demo Complete. Press Ctrl+C to exit.[/bold cyan]")

    # Keep alive to allow inspecting the dashboard or API if needed, or just exit.
    # For a CLI tool, exiting is usually better, but for a "dashboard" seeing the result is good.
    # The Live context manager handles the display. We can just exit.

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting...[/yellow]")
