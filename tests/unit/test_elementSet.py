"""_summary_
"""

import pytest
import fwoptimizer.utils.elementSet as e

def test_registry():

    expectedRegistred = ['ElementSet', 'DirSet', 'ProtSet']
    
    for i in expectedRegistred:

        assert i in e.ElementSetRegistry.getRegistry().keys()




