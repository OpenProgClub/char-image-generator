from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

from itertools import chain


class FontInfo:
    def __init__(self, font_path):
        self.ttf = TTFont(font_path, 0, allowVID=0,
                          ignoreDecompileErrors=True,
                          fontNumber=0)
        self.chars = chain.from_iterable(
            [y + (Unicode[y[0]],) for y in x.cmap.items()]
            for x in self.ttf['cmap'].tables)
        self.codes = [_[0] for _ in self.chars]

    def is_char_exist(self, char):
        code = ord(char)
        return code in self.codes

    def is_all_chars_exist(self, char_list):
        for char in char_list:
            if not self.char_exists(char):
                return False
        return True
