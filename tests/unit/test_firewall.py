"""
Tests for the Field, FieldList and Firewall classes
"""

import fwoptimizer.core.firewall as f

sampleInput = 'tests/test_fdd_config.toml'

expectedOutput =  [
    {'name' : 'SrcIP', 'type' : 'DirectionSet'},
    {'name' : 'DstIP', 'type' : 'DirectionSet'},
    {'name' : 'Protocol', 'type' : 'ProtocolSet'}
]

def test_fieldList():
    """_summary_
    """

    fieldList = f.FieldList()
    fieldList.loadConfig(sampleInput)
    fields = fieldList.getFields()

    for i, field in enumerate(fields):

        assert field.getName() == expectedOutput[i]['name']
        assert field.getType() == expectedOutput[i]['type']
