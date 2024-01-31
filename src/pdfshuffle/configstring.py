class ConfigString:
    _data = None

    def __init__(self, data, typ=str):
        self.set(data, typ=typ)

    def set(self, data, typ=str):
        if typ == str:
            if isinstance(data, str):
                self._data = data
            elif isinstance(data, int):
                self._data = str(data)
            else:
                raise TypeError("Data must be only Int, Str")
        elif typ == int:
            if isinstance(data, int):
                self._data = data
            elif isinstance(data, str):
                try:
                    self._data = int(data)
                except ValueError:
                    self._data = 0
            else:
                raise TypeError("Data cannot be converted")
        elif typ == list:
            if isinstance(data, list):
                self._data = data
            else:
                self._data = list(data)
        else:
            raise TypeError("Data must be only Int, Str or List!")

    def get(self):
        return self.__str__()

    def __repr__(self):
        return f'{self.__class__.__name__}(type_{type(self._data)})={self._data}'

    def __str__(self):
        if isinstance(self._data, int):
            return str(self._data)
        elif isinstance(self._data, str):
            return self._data
        elif isinstance(self._data, list):
            return ','.join(self._data)

    def __eq__(self, y):
        if isinstance(y, type(self._data)):
            return self._data == y
        else:
            raise TypeError("Not equal type objects")

    def __hash__(self):
        return hash(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        if isinstance(self._data, int):
            return self._data
        else:
            return self._data[key]

    def __setitem__(self, key, value):
        if isinstance(self._data, list):
            self._data[key] = value
        else:
            raise TypeError("Object initial no list type...")
