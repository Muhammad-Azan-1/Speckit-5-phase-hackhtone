"""Unit tests for dependency management functionality."""
import sys
from unittest.mock import patch
from io import StringIO
import pytest

# Add the src directory to the path so we can import the module
sys.path.insert(0, 'src')

from todo_cli.main import main


def test_rich_dependency_available():
    """Test that the rich dependency is available and can be imported."""
    try:
        import rich
        assert rich is not None
    except ImportError:
        pytest.fail("Rich dependency is not available")


def test_rich_functionality():
    """Test that rich functionality works as expected."""
    from rich.console import Console
    from rich.panel import Panel

    # Test that we can create a console and panel
    console = Console()
    panel = Panel("Test content")

    # Verify they're the correct types
    assert isinstance(console, Console)
    assert isinstance(panel, Panel)