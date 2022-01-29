class ObjectFactory:

    def __init__(self):
        self._objects = {}

    def register_object(self, alias, object):
        self._objects[alias] = object

    def create(self, alias):
        object = self._objects.get(alias)
        if not object:
            raise ValueError(alias)
        return object()



