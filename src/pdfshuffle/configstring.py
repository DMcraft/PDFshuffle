class ConfigString:
    """
    Класс для хранения и управления данными (str, int, list), с поддержкой базовых операций.
    Предназначен для использования в конфигурациях или при работе с гетерогенными данными.
    """

    _data = None

    def __init__(self, data, typ=str):
        """
        Инициализирует объект ConfigString, сохраняя данные указанного типа.

        :param data: Значение, которое нужно сохранить.
        :param typ: Тип данных (str, int, list).
        """
        self.set(data, typ=typ)

    def set(self, data, typ=str):
        """
        Устанавливает значение и его тип.

        :param data: Значение, которое нужно сохранить.
        :param typ: Тип данных (str, int, list).
        :raises TypeError: Если тип не поддерживается или данные некорректны.
        """
        if not isinstance(typ, type):
            raise TypeError("Тип должен быть классом, а не экземпляром.")

        if typ == str:
            if isinstance(data, str):
                self._data = data
            elif isinstance(data, int):
                self._data = str(data)
            else:
                raise TypeError("Данные должны быть строкой или целым числом.")
        elif typ == int:
            if isinstance(data, int):
                self._data = data
            elif isinstance(data, str):
                try:
                    self._data = int(data)
                except ValueError as e:
                    self._data = 0
                    raise ValueError(f"Невозможно преобразовать строку '{data}' в int") from e
            else:
                raise TypeError("Некорректный тип данных для int.")
        elif typ == list:
            if isinstance(data, list):
                self._data = data
            else:
                try:
                    self._data = list(data)
                except TypeError as e:
                    raise TypeError(f"Невозможно привести '{data}' к списку") from e
        else:
            raise TypeError("Поддерживаются только типы str, int, list.")

    def get(self):
        """
        Возвращает оригинальные данные без преобразования.

        :return: Хранящиеся данные.
        """
        return self._data

    def __repr__(self):
        """
        Возвращает строковое представление объекта, удобное для отладки.
        """
        return f"{self.__class__.__name__}({type(self._data).__name__}, {self._data!r})"

    def __str__(self):
        """
        Возвращает строковое представление данных.

        :return: Строка, представляющая содержимое.
        :raises TypeError: Если данные нельзя преобразовать в строку.
        """
        if isinstance(self._data, str):
            return self._data
        elif isinstance(self._data, int):
            return str(self._data)
        elif isinstance(self._data, list):
            return ','.join(str(x) for x in self._data)
        raise TypeError(f"Невозможно преобразовать {type(self._data)} в строку")

    def __eq__(self, other):
        """
        Сравнивает текущий объект с другим объектом ConfigString или с базовым типом.

        :param other: Объект для сравнения.
        :return: True, если данные равны, иначе False.
        """
        if isinstance(other, ConfigString):
            return self._data == other._data
        return self._data == other

    def __hash__(self):
        """
        Возвращает хэш-значение данных, если они хешируемы.

        :return: Хэш-значение.
        :raises TypeError: Если данные не хешируемы.
        """
        return hash(tuple(self._data)) if isinstance(self._data, list) else hash(self._data)

    def __len__(self):
        """
        Возвращает длину данных, если применимо.

        :return: Длина данных.
        :raises TypeError: Если данные не поддерживают длину.
        """
        return len(self._data)

    def __getitem__(self, key):
        """
        Получает элемент по индексу, если данные — список.

        :param key: Индекс.
        :return: Элемент списка.
        :raises TypeError: Если данные не являются списком.
        :raises IndexError: Если индекс вне диапазона.
        """
        if not isinstance(self._data, list):
            raise TypeError("Доступ по индексу доступен только для списков")
        return self._data[key]

    def __setitem__(self, key, value):
        """
        Устанавливает значение по индексу, если данные — список.

        :param key: Индекс.
        :param value: Новое значение.
        :raises TypeError: Если данные не являются списком.
        :raises IndexError: Если индекс вне диапазона.
        """
        if not isinstance(self._data, list):
            raise TypeError("Изменение по индексу доступно только для списков")
        self._data[key] = value