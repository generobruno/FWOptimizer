"""_summary_
"""

from collections.abc import Iterable
from collections import defaultdict

class AliasDefaultDict:
    """_summary_
    """

    def __init__(self, default_factory, initial=None):
        """
        Create a new AliasDefaultDictionary

        Args:
            default_factory (_type_): _description_
            initial (list, optional): _description_. Defaults to [].
        """
        if initial is None:
            initial = []
        
        self.aliases = {}
        self.data = {}
        self.factory = default_factory
        
        for aliases, value in initial:
            self[aliases] = value

    @staticmethod
    def distinguishKeys(key):
        """_summary_

        Args:
            key (_type_): _description_

        Returns:
            _type_: _description_
        """
        if isinstance(key, Iterable) and not isinstance(key, str):
            return set(key)
        
        return {key}

    def __getitem__(self, key):
        """_summary_

        Args:
            key (_type_): _description_

        Returns:
            _type_: _description_
        """
        keys = self.distinguishKeys(key)
        if keys & self.aliases.keys():
            return self.data[self.aliases[keys.pop()]]

        value = self.factory()
        self[keys] = value
        return value

    def __setitem__(self, key, value):
        """Sets the value for the given key or keys.

        Args:
            key: A single key or an iterable of keys.
            value: The value to set.

        Returns:
            value: The value that was set.
        """
        keys = self.distinguishKeys(key)
        if keys & self.aliases.keys():
            self.data[self.aliases[keys.pop()]] = value
        else:
            new_key = object()
            self.data[new_key] = value
            for alias in keys:
                self.aliases[alias] = new_key
            return value
        
        return None

    def __repr__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        representation = defaultdict(list)
        for alias, value in self.aliases.items():
            representation[value].append(alias)
        return f"AliasDefaultDict({repr(self.factory)}, {repr([(aliases, self.data[value]) for value, aliases in representation.items()])})"

    def get(self, key, default=None):
        """
        AliasDefaultDict get option value
        """
        keys = self.distinguishKeys(key)
        if keys & self.aliases.keys():
            return self.data[self.aliases[keys.pop()]]
        
        return default
