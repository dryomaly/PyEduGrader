import os
import sys
from src.grader import StudentCodeAnalyzer

# Ensure python can find the src module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create a temporary dummy file for testing
TEST_FILE = "temp_test_code.py"


def setup_module():
    with open(TEST_FILE, "w") as f:
        f.write("def good_function():\n")
        f.write("    '''This is a docstring.'''\n")
        f.write("    return True\n\n")
        f.write("def badFunction():\n")
        f.write("    return False\n")


def teardown_module():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_grader_scoring():
    analyzer = StudentCodeAnalyzer(TEST_FILE)
    result = analyzer.analyze()

    # Initial 100
    # - 10 (badFunction missing docstring)
    # - 5 (badFunction naming)
    # = 85
    assert result["score"] == 85


def test_issues_list():
    analyzer = StudentCodeAnalyzer(TEST_FILE)
    result = analyzer.analyze()
    assert len(result["issues"]) == 2
    issue_text = "Function 'badFunction' should be in snake_case."
    assert issue_text in result["issues"]


def test_file_not_found():
    analyzer = StudentCodeAnalyzer("non_existent.py")
    assert "error" in analyzer.analyze()
