"""_summary_
"""

import toml


class Field:
    """_summary_
    """

    def __init__(self, name, type):
        """_summary_

        Args:
            name (_type_): _description_
            type (_type_): _description_
        """
        self._name_ = name
        self._type_ = type

    def getName(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._name_

    def getType(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._type_



class FieldList:
    """_summary_
    """

    def __init__(self):
        """_summary_
        """
        self._fields_ = []

    def loadConfig(self, path):
        """_summary_

        Args:
            path (_type_): _description_
        """

        config = toml.load(path)

        _fields_ = config['fdd_config']['fields']

        for field in _fields_:
            self._fields_.append(Field(field['name'], field['type']))

    def getFields(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._fields_

    def printCofig(self):
        """_summary_
        """
        for i in range(len(self._fields_)):
            print(f'{i} [{self._fields_[i].getName()}, {self._fields_[i].getType()}]')



class Firewall:
    """_summary_
    """
