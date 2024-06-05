import json

with open('pylint_out.json', encoding="utf-8") as f:
    reports = json.load(f)

for report in reports:
    if report['type'] == 'warning':
        print(f"::warning file={report['path']},line={report['line']},col={report['column']}::{report['message']}")
    elif report['type'] == 'error':
        print(f"::error file={report['path']},line={report['line']},col={report['column']}::{report['message']}")
