import ast
import os


class StudentCodeAnalyzer:
    """
    Analyzes student code for educational quality metrics:
    1. Docstrings presence (students must document code).
    2. Function length (students should write concise functions).
    3. Naming conventions (snake_case for functions).
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.report = {
            "score": 100,
            "issues": []
        }

    def analyze(self):
        if not os.path.exists(self.file_path):
            return {"error": "File not found"}

        with open(self.file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self._check_docstring(node)
                self._check_function_length(node)
                self._check_naming(node)

        return self.report

    def _check_docstring(self, node):
        """Penalty if a function has no docstring."""
        if not ast.get_docstring(node):
            self.report["score"] -= 10
            self.report["issues"].append(
                f"Function '{node.name}' is missing a docstring."
            )

    def _check_function_length(self, node):
        """Penalty if a function is too long (>15 lines)."""
        length = node.end_lineno - node.lineno
        if length > 15:
            self.report["score"] -= 5
            self.report["issues"].append(
                f"Function '{node.name}' is too long ({length} lines)."
            )

    def _check_naming(self, node):
        """Penalty if function name is not snake_case."""
        is_snake = node.name.islower() or "_" in node.name
        if not is_snake and node.name != node.name.lower():
            self.report["score"] -= 5
            self.report["issues"].append(
                f"Function '{node.name}' should be in snake_case."
            )
