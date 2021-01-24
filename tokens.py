class Tokens(object):
    def __init__(self, text, pos, tag):
        self._text = text
        self._pos = pos
        self._tag = tag

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @text.deleter
    def text(self):
        del self._text

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @pos.deleter
    def pos(self):
        del self._pos

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        self._tag = tag

    @tag.deleter
    def tag(self):
        del self._tag
