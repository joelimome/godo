
class odict(dict):
    """\
    A dict class that tracks the order in which keys
    are defined.
    """

    def __init__(self, *args, **kwargs):
        self.key_order = []
        super(odict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if key in self.key_order:
            self.key_order.remove(key)
        self.key_order.append(key)
        return super(odict, self).__setitem__(key, value)

    def __delitem__(self, key):
        if key in self.key_order:
            self.key_order.remove(key)
        return super(odict, self).__delitem__(key)

    def iteritems(self):
        for k in self.key_order:
            yield (k, self[k])