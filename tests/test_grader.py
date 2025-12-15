import os
from src.grader import StudentCodeAnalyzer

# Create a temporary dummy file for testing
TEST_FILE = "temp_test_code.py"


def setup_module():
    with open(TEST_FILE, "w") as f:
        f.write("""
def good_function():
    '''This is a docstring.'''
    return True

def badFunction():
    return False
""")


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
    assert "Function 'badFunction' should be in snake_case." in result["issues"]


def test_file_not_found():
    analyzer = StudentCodeAnalyzer("non_existent.py")
    assert "error" in analyzer.analyze()
