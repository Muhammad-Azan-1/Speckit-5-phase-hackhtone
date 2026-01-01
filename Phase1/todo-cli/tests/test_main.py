"""Unit tests for the main module of Todo-CLI application."""
import sys
from io import StringIO
from unittest.mock import patch
import pytest

# Add the src directory to the path so we can import the module
sys.path.insert(0, 'src')

from todo_cli.main import main


def test_main_function():
    """Test that the main function runs without errors."""
    # Capture stdout to check output
    with patch('sys.stdout', new=StringIO()) as fake_out:
        main()
        output = fake_out.getvalue()

    # Check that some output was produced
    assert "Todo-CLI" in output