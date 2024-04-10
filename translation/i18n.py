'''
example:
xxxxx.aaa.ccc=abcd\n acbd
'''
import re


class I18n:
    def __init__(self):
        self.translations = {}
        for lang in ['en_US', 'zh_CN']:
            self.read(lang)
        self.lang = 'en_US'
    def read(self, lang):
        def parseLang(lang):
            result = {}
            cacheKey = ''
            cacheIndent = 2
            for line in lang.split('\n'):
                if not line.strip() or line.strip().startswith('#'):
                    continue
                if cacheKey:
                    if line.startswith(' ' * cacheIndent):
                        result[cacheKey] += '\n' + line.replace(' ' * cacheIndent, '', 1)
                        continue
                    cacheKey = ''
                    cacheIndent = 2
                key, value = line.split('=', 1)
                if re.match(r'^\|\d*$', value):
                    cacheKey = key
                    cacheIndent = int(value.split('|', 1)[1]) if value.split('|', 1)[1] else 2
                    result[key] = ''
                    continue
                value = value.split('#', 1)[0].strip()
                result[key] = value.replace('\\n', '\n')
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