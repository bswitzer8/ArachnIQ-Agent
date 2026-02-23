import time
import threading
import uvicorn
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich import box

from app.mock_api import app
from app.generator import TestGenerator
from app.runner import TestRunner

load_dotenv()
console = Console()

def run_api():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

def main():
    console.print(Panel("[bold cyan]ArachnIQ-Agent: AI-Powered API Testing Demo[/bold cyan]", box=box.DOUBLE))
    
    # 1. Start Mock API
    console.print("[yellow]Starting Mock API...[/yellow]")
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    time.sleep(2) # Give it a moment to start
    
    # 2. Generate Tests
    console.print("[yellow]Asking Gemini to generate test cases based on API schema...[/yellow]")
    schema = """
    Endpoints:
    - GET /: Welcome message.
    - POST /users/register: {username, email}. Bug: No duplicate check.
    - GET /products: List products.
    - GET /products/{product_id}: Details. Bug: Exception on ID 999.
    - POST /cart/add: {product_id, quantity}. Bug: Allows negative quantity.
    - POST /checkout: Process cart. Bug: Fails if > 5 items.
    """
    
    try:
        generator = TestGenerator()
        test_cases = generator.generate_tests(schema)
        console.print(f"[green]Successfully generated {len(test_cases)} test cases.[/green]")
    except Exception as e:
        console.print(f"[red]Error during generation: {e}[/red]")
        return

    # 3. Run Tests with Live Dashboard
    runner = TestRunner(base_url="http://localhost:8000")
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
    
    console.print("
[bold]Test Summary:[/bold]")
    console.print(f"Total: {len(results)}")
    console.print(f"Passed: [green]{passed_count}[/green]")
    console.print(f"Failed: [red]{failed_count}[/red]")
    
    # 5. Generate Reports
    json_rep, md_rep = runner.generate_reports()
    console.print(f"
[bold blue]Reports generated:[/bold blue]")
    console.print(f"- JSON: {json_rep}")
    console.print(f"- Markdown: {md_rep}")

if __name__ == "__main__":
    main()
