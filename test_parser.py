import json
import os
import time
from typing import Any, Dict, Tuple
import pytest
import jsonparser


@pytest.fixture
def test_files():
    """Get all JSON test files from test_cases directory."""
    test_dir = "test_cases"
    return [f for f in os.listdir(test_dir) if f.endswith(".json")]


def test_parser_against_builtin(test_files):
    """
    Compare jsonparser.loads output against json.loads for all test cases.

    This test ensures our implementation produces identical results to the
    built-in json module for all test cases.
    """
    test_dir = "test_cases"

    for filename in sorted(test_files):
        print(f"\nTesting {filename}")

        # Load test case
        with open(os.path.join(test_dir, filename), "r") as f:
            content = f.read()

        # Parse with both parsers
        expected = json.loads(content)
        result = jsonparser.loads(content)

        # Compare results with detailed diff
        assert result == expected, (
            f"\nParser output mismatch in {filename}\n"
            f"Expected:\n{expected}\n"
            f"Got:\n{result}\n"
            f"Raw content:\n{content[:200]}..."  # Show first 200 chars of raw content
        )
        print(f"✓ {filename} passed")


def test_performance_comparison(test_files):
    """
    Compare performance between jsonparser.loads and json.loads.

    This test measures and compares the execution time of both parsers
    across all test cases.
    """
    test_dir = "test_cases"
    results = {"builtin": {"time": 0.0}, "custom": {"time": 0.0}}

    for filename in sorted(test_files):
        with open(os.path.join(test_dir, filename), "r") as f:
            content = f.read()

        # Time built-in parser
        start = time.perf_counter()
        json.loads(content)
        results["builtin"]["time"] += time.perf_counter() - start

        # Time custom parser
        start = time.perf_counter()
        jsonparser.loads(content)
        results["custom"]["time"] += time.perf_counter() - start

    # Print performance summary
    print("\n=== Performance Summary ===")
    print(f"Total test files: {len(test_files)}")
    print(f"Built-in json:   {results['builtin']['time']:.6f} seconds")
    print(f"Custom parser:   {results['custom']['time']:.6f} seconds")
    print(
        f"Relative speed:  {results['builtin']['time']/results['custom']['time']:.2f}x"
    )
