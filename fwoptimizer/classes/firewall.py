"""_summary_
"""

import toml


class Field:
    """_summary_
    """
    
    def __init__(self, name, type):
        self._name_ = name
        self._type_ = type

    def getName(self):
        return self._name_
    
    def getType(self):
        return self._type_



class FieldList:
    """_summary_
    """
    
    def __init__(self):
        self._fields_ = []

    def loadConfig(self, path):

        config = toml.load(path)

        _fields_ = config['fdd_config']['fields']

        for field in _fields_:
            self._fields_.append(Field(field['name'], field['type']))

    def getFields(self):
        return self._fields_

    def printCofig(self):
        
        for i in range(len(self._fields_)):
            print(f'{i} [{self._fields_[i].getName()}, {self._fields_[i].getType()}]')



class Firewall:
    """_summary_
    """
    pass




