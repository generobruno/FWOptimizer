"""_summary_
"""

import fwoptimizer.utils.elementSet as e

def test_registry():
    """_summary_
    """

    expectedRegistred = ['ElementSet', 'DirSet', 'ProtSet']
    
    for i in expectedRegistred:

        assert i in e.ElementSetRegistry.getRegistry().keys()
