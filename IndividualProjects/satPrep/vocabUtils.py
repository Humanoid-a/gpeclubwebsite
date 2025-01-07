class VocabSet(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_defs(self, word):
        return self[word]

    def get_words(self):
        return self.keys()
