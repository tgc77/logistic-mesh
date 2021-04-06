from collections import defaultdict


class Graph:
    """ Basic graph implementation  . """

    def __init__(self):
        """Initialize graph structures."""
        self._adjacents = defaultdict(dict)
        self._vertices = set()

    def load_from_json(self, json):
        for routes in json:
            if len(routes) == 0:
                continue
            self._adjacents[routes[0]].update({routes[1]: routes[2]})
            self._vertices.add(routes[0])
            self._vertices.add(routes[1])
        self._vertices = list(self.vertices)
        self._vertices.sort()

    @property
    def adjacents(self):
        return self._adjacents

    @property
    def vertices(self):
        return self._vertices

    def __len__(self):
        return len(self._adjacents)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._adjacents))

    def __getitem__(self, v):
        return self._adjacents[v]
