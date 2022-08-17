from urllib.parse import urlsplit


class Url:
    def __init__(self, url):
        parts = urlsplit(url)

        if not parts.scheme or parts.scheme == "":
            self.scheme = "http"
            paths = parts.path.strip('/').split('/')
            self.hostname = paths[0]
            if len(paths) > 1:
                self.paths = paths[1:]
            else:
                self.paths = []
        else:
            self.scheme = parts.scheme
            self.hostname = parts.hostname
            self.paths = parts.path.strip('/').split('/')

        self.paths = list(filter(None, self.paths))

        if self.hostname.startswith("www."):
            self.hostname = self.hostname.replace("www.", "")

        self.fragment = parts.fragment

        self.queries = {}
        queries = parts.query.strip('&').split('&')
        queries = list(filter(None, queries))

        for query in queries:
            pair = query.strip('=').split('=')
            self.queries[pair[0]] = pair[1]

    def __str__(self):
        str = self.scheme + "://"
        str = str + self.hostname
        if self.paths and len(self.paths) != 0:
            for path in self.paths:
                str = str + '/' + path
        return str

    def full(self) -> str:
        str = self.scheme + "://"
        str = str + self.hostname

        if len(self.paths) != 0:
            for path in self.paths:
                str = str + '/' + path

        if len(self.queries) != 0:
            str = str + '?'
            for key in self.queries:
                str = str + key + '=' + self.queries[key]

        if self.fragment and self.fragment != '':
            str = str + "#" + self.fragment
        return str

    def __eq__(self, other):
        if not isinstance(other, Url) and not isinstance(other, str):
            raise NotImplementedError(self.__class__.__name__ + '.try_something')

        if isinstance(other, str):
            other = Url(other)

        if self.hostname != other.hostname:
            return False
        if self.paths != other.paths:
            return False

        return True
