import xml.etree.ElementTree as ET

tree = ET.parse('.github/pytest_out.xml')
root = tree.getroot()

for testcase in root.findall('.//testcase'):
    file_attr = testcase.attrib.get('file', 'unknown')
    line_attr = testcase.attrib.get('line', '0')
    for failure in testcase.findall('failure'):
        print(f"::error file={file_attr},line={line_attr}::{failure.text}")
    for warning in testcase.findall('warning'):
        print(f"::warning file={file_attr},line={line_attr}::{warning.text}")