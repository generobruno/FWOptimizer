"""
Tests for the Field, FieldList and Firewall classes
"""

import pytest
import fwoptimizer.classes.firewall as f

sampleInput = 'tests/test_fdd_config.toml'

expected_output =  [
    {'name' : 'SrcIP', 'type' : 'DirSet'},
    {'name' : 'DstIP', 'type' : 'DirSet'},
    {'name' : 'Protocol', 'type' : 'ProtSet'}
]

def test_fieldList():

    fieldList = f.FieldList()
    fieldList.loadConfig(sampleInput)
    fields = fieldList.getFields()

    for i in range(len(fields)):

        assert fields[i].getName() == expected_output[i]['name']
        assert fields[i].getType() == expected_output[i]['type']


    
