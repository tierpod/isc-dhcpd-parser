class Function(object):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return "Function({name}{args})".format(**self.__dict__)


class Item(object):
    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return "Item{values}".format(**self.__dict__)

    def __contains__(self, item):
        return item in self.values


class ItemSet(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return "ItemSet({key} = {value})".format(**self.__dict__)

    def __contains__(self, item):
        return item in self.key


class Section(object):
    def __init__(self, key, data):
        self.key = key
        self.data = data

    def __repr__(self):
        return "Section({key}, {length}, {data})".format(key=self.key, length=len(self.data),
                                                         data=self.data)
