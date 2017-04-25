import os


class Characters:
    class SubChars:
        def __init__(self, name, codes=None):
            self.name = name
            self.codes = codes

    hiragana = SubChars('hiragana', list(range(12353, 12439)))

    hiragana_basic_list = [ord(c) for c in 'あぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろわをん']
    hiragana_basic = SubChars('hiragana-basic', hiragana_basic_list)

    katakana = SubChars('katakana', list(range(12449, 12539)))

    katakana_basic_list = [ord(c) for c in 'ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワンヵヶ']
    katakana_basic = SubChars('katakana-basic', katakana_basic_list)

    alphabet_list = list(range(65, 91)) + list(range(97, 123))
    alphabets = SubChars('alphabets', alphabet_list)

    digits = SubChars('digits', list(range(48, 58)))
    han_digits = SubChars('han-digits', [ord(c) for c in '〇一二三四五六七八九'])

    # Top 200 kanji from Wikipedia
    kanji_200_list = [ord(c) for c in '年日月大本学人国中一市出部会作名地行道生時子田上東県場山合第代社高戦後事者用画発手長駅川分業間立物校線新所関成前小目車動内同送野和主自開定文町放号通家京島的連選体下番方機公村世現入在設全北回記外式原表三海平化女明度区語神組法曲当西数位最教鉄対都力軍理初性見水書多期以品員演特身電実民元要金木政制治等経正勝南面州使形編王空科口置優点映天二共楽界岡加能気音像美売版話路系知来賞務重井取言参次信局称活台松運']
    kanji_200 = SubChars('kanji-200', kanji_200_list)

    module_dir = os.path.dirname(__file__)
    with open(os.path.join(module_dir, 'joyo-kanji.txt'), 'r') as f:
        txt = f.read().strip()
    kanji_joyo_list = [ord(c) for c in txt]
    kanji_joyo = SubChars('kanji-joyo', kanji_joyo_list)

    @classmethod
    def combine_codes(cls, subchar_list):
        codes = []
        for subchar in subchar_list:
            codes += getattr(cls, subchar).codes
        return codes
