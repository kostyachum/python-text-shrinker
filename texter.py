import json

ANALYZE_TYPE_WORD = ' '
ANALYZE_TYPE_SENTENCE = '.'
ANALYZE_TYPE_LINE = '\n'
ANALYZE_TYPE_TAB = '\t'

ANALYZE_TYPE_WORD_NAME = 'word'
ANALYZE_TYPE_SENTENCE_NAME = 'sentence'
ANALYZE_TYPE_LINE_NAME = 'line'
ANALYZE_TYPE_TAB_NAME = 'tab'

ANALYZE_OPTIONS = (
    (ANALYZE_TYPE_WORD_NAME, 'Word'),
    (ANALYZE_TYPE_SENTENCE_NAME, 'Sentence'),
    (ANALYZE_TYPE_LINE_NAME, 'Line'),
    (ANALYZE_TYPE_TAB_NAME, 'Tab')
)


ANALYZE_NAME_TO_VALUE_MAP = {
    ANALYZE_TYPE_WORD_NAME: ANALYZE_TYPE_WORD,
    ANALYZE_TYPE_SENTENCE_NAME: ANALYZE_TYPE_SENTENCE,
    ANALYZE_TYPE_LINE_NAME: ANALYZE_TYPE_LINE,
    ANALYZE_TYPE_TAB_NAME: ANALYZE_TYPE_TAB,
}

ANALYZE_LAYOUT_MAP = {
    ANALYZE_TYPE_WORD_NAME: '&nbsp;',
    ANALYZE_TYPE_SENTENCE_NAME: '.',
    ANALYZE_TYPE_LINE_NAME: '<br>',
    ANALYZE_TYPE_TAB_NAME: '&emsp',
}


class Entity:
    def __init__(self, string):
        self.string = string


class CharAnalyzer:
    ignore_chars = ' ,./;"[]{}!@#$%^&*()_+~`?><:"|-\'\n\t'

    def __init__(self, text):
        self.text = text
        self.char_stat_total = {}
        self.char_stat_relative = {}
        self.total_chars = 0

        self.collect_total_char_stat()
        self.calculate_relative_char_stat()

    def get_stat_keys(self):
        return list(self.char_stat_relative.keys())

    def get_stat_values(self):
        return ["{0:.2f}".format(value) for value in self.char_stat_relative.values()]

    def get_json(self):
        return json.dumps([{'label': key, 'value': "{0:.2f}".format(value), 'source': 'origin'} for key, value in self.char_stat_relative.items()])

    def collect_total_char_stat(self):
        for ch in self.text:
            ch = ch.lower()
            if ch in self.ignore_chars:
                continue
            self.char_stat_total[ch] = self.char_stat_total.get(ch, 0) + 1
            self.total_chars += 1

    def calculate_relative_char_stat(self):
        for key, value in self.char_stat_total.items():
            self.char_stat_relative[key] = 100.0 / self.total_chars * value


class Texter:

    def __init__(self, source_text, analyze_type):
        self.source_text = source_text
        self.analyze_type_name = analyze_type
        self.analyze_type = ANALYZE_NAME_TO_VALUE_MAP.get(analyze_type)
        self.analyze_type_layout = ANALYZE_LAYOUT_MAP.get(analyze_type)
        if not self.analyze_type:
            raise ValueError('{} is not available analyze type'.format(analyze_type))

        self.analyzed_source = CharAnalyzer(source_text)
        self.analyzed_entities = None

    def analyze_entities(self):
        self.analyzed_entities = [CharAnalyzer(chunk.strip()) for chunk in self.source_text.split(self.analyze_type)]
