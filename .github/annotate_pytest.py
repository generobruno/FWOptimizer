import xml.etree.ElementTree as ET
import re

def extract_file_line_from_failure(failure_text):
    match = re.search(r'File "(.*?)", line (\d+)', failure_text)
    if match:
        return match.group(1), match.group(2)
    return "unknown", "0"

tree = ET.parse('.github/pytest_out.xml')
root = tree.getroot()

for testcase in root.findall('.//testcase'):
    classname = testcase.attrib.get('classname', 'unknown')
    name = testcase.attrib.get('name', 'unknown')
    file_attr = "unknown"
    line_attr = "0"
    for failure in testcase.findall('failure'):
        failure_text = failure.text
        file_attr, line_attr = extract_file_line_from_failure(failure_text)
        message = failure_text.strip().replace("\n", "%0A")
        print(f"::error file={file_attr},line={line_attr}::{message}")
    for warning in testcase.findall('warning'):
        warning_text = warning.text
        file_attr, line_attr = extract_file_line_from_failure(warning_text)
        message = warning_text.strip().replace("\n", "%0A")
        print(f"::warning file={file_attr},line={line_attr}::{message}")