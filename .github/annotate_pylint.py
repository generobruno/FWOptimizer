"""
Annotate Pylint warnings and errors in github actions
"""

import json

with open('.github/pylint_out.json', encoding="utf-8") as f:
    reports = json.load(f)

for report in reports:
    if report['type'] == 'warning':
        print(
            f"::warning file={report['path']},"
            f"line={report['line']},"
            f"col={report['column']}::{report['message']}"
        )
    elif report['type'] == 'error':
        print(
            f"::error file={report['path']},"
            f"line={report['line']},"
            f"col={report['column']}::{report['message']}"
        )
