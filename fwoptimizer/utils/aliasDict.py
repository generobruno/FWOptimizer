"""_summary_
"""

from collections.abc import Iterable
from collections import defaultdict

class AliasDefaultDict:
    """_summary_
    """
    
    def __init__(self, default_factory, initial=[]):
        """_summary_

        Args:
            default_factory (_type_): _description_
            initial (list, optional): _description_. Defaults to [].
        """
        self.aliases = {}
        self.data = {}
        self.factory = default_factory
        
        for aliases, value in initial:
            self[aliases] = value
            
    @staticmethod
    def distinguish_keys(key):
        """_summary_

        Args:
            key (_type_): _description_

        Returns:
            _type_: _description_
        """
        if isinstance(key, Iterable) and not isinstance(key, str):
            return set(key)
        else:
            return {key}
        
    def __getitem__(self, key):
        """_summary_

        Args:
            key (_type_): _description_

        Returns:
            _type_: _description_
        """
        keys = self.distinguish_keys(key)
        if keys & self.aliases.keys():
            return self.data[self.aliases[keys.pop()]]
        else:
            value = self.factory()
            self[keys] = value
            return value
    
    def __setitem__(self, key, value):
        """_summary_

        Args:
            key (_type_): _description_
            value (_type_): _description_

        Returns:
            _type_: _description_
        """
        keys = self.distinguish_keys(key)
        if keys & self.aliases.keys():
            self.data[self.aliases[keys.pop()]] = value
        else:
            new_key = object()
            self.data[new_key] = value
            for key in keys:
                self.aliases[key] = new_key
            return value
        
    def __repr__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        representation = defaultdict(list)
        for alias, value in self.aliases.items():
            representation[value].append(alias)
        return "AliasDefaultDict({}, {})".format(repr(self.factory), repr([(aliases, self.data[value]) for value, aliases in representation.items()]))