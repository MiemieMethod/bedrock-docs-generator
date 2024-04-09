

class I18n:
    def __init__(self):
        self.translations = {}
        for lang in ['en_US', 'zh_CN']:
            self.read(lang)
        self.lang = 'en_US'
    def read(self, lang):
        def parseLang(lang):
            result = {}
            for line in lang.split('\n'):
                if line.startswith('#') or not line.strip():
                    continue
                key, value = line.split('=', 1)
                value = value.split('#', 1)[0].strip()
                result[key] = value
            return result

        with open(r'assets/translations/{}.lang'.format(lang), 'r', encoding='utf-8') as f:
            self.translations[lang] = parseLang(f.read())

    def setLang(self, lang):
        self.lang = lang

    def get(self, key):
        return self.translations[self.lang].get(key, key.replace('<', '&lt;').replace('>', '&gt;'))

    def contain(self, key):
        return key in self.translations[self.lang]


i18n = I18n()
i18n.setLang('zh_CN')