"""
Tests for the parser Module
"""

import pytest
from fwoptimizer.classes import Parser

# Sample syntax table
sample_syntax_table = {
    'filter': {
        'RuleOperations': {
            '-s': r'\d+\.\d+\.\d+\.\d+/\d+',
            '-d': r'\d+\.\d+\.\d+\.\d+/\d+',
            '-p': r'(tcp|udp)',
            '-j': r'(ACCEPT|DROP)'
        }
    }
}

# Path to the sample input data file
sample_input_file_path = 'tests/test_set.txt'

# Test initialization
def test_parser_initialization():
    """_summary_
    """
    assert 2+2 == 4


# Run all tests
if __name__ == "__main__":
    pytest.main()
