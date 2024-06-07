"""_summary_
"""

import toml


class Field:
    """_summary_
    """

    def __init__(self, fieldName, fieldType):
        """_summary_

        Args:
            fieldName (_type_): _description_
            fieldType (_type_): _description_
        """
        self._fieldName_ = fieldName
        self._fieldType_ = fieldType

    def getName(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._fieldName_

    def getType(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._fieldType_



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
        for i, field in enumerate(self._fields_):
            print(f'{i} [{field.getName()}, {field.getType()}]')



class Firewall:
    """_summary_
    """
