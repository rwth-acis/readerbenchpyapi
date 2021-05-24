import json
from rb_api.json_serialize import JsonSerialize

class TextualComplexityDataDTO(JsonSerialize):

    def __init__(self, lang, level, texts, categoriesList, complexityIndices):
        self.lang = lang
        self.texts = texts
        self.list = categoriesList
        self.complexityIndices = complexityIndices
        self.level = level

    def __str__(self):
        return "TextualComplexityData (lang=%s, level='%s'):\nCategories=%s\nIndices=%s" % (self.lang, self.level, self.list, self.complexityIndices)

    def serialize(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.serialize()

    @staticmethod
    def dumper(obj):
        if "serialize" in dir(obj):
            return obj.serialize()

        return obj.__dict__
