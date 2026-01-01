"""Integration tests for complete project functionality."""
import sys
import subprocess
from unittest.mock import patch
from io import StringIO
import pytest

# Add the src directory to the path so we can import the module
sys.path.insert(0, 'src')

from todo_cli.main import main


def test_main_function_runs_without_error():
    """Test that the main function runs without errors."""
    # Capture stdout to check output
    with patch('sys.stdout', new=StringIO()) as fake_out:
        main()
        output = fake_out.getvalue()

    # Check that expected output was produced
    assert "Todo-CLI application" in output
    assert "Use --help" in output


def test_cli_execution():
    """Test that the CLI executes properly."""
    # Run the application using subprocess
    result = subprocess.run(['uv', 'run', 'todo-cli'],
                          capture_output=True, text=True, timeout=10)

    # Check that it ran successfully
    assert result.returncode == 0
    assert "Todo-CLI application" in result.stdout