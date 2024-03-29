

class Markdown(object):

    def __init__(self):
        self.components = []

    def addComponent(self, component):
        self.components.append(component)

    def render(self):
        return '\n'.join([c.render() for c in self.components])


class MarkdownComponent(object):

        def render(self):
            return ''


class MarkdownText(MarkdownComponent):

        def __init__(self, text):
            self.text = text

        def render(self):
            return self.text + '\n'


class MarkdownCodeBlock(MarkdownComponent):

            def __init__(self, code, language=None):
                self.code = code
                self.language = language

            def render(self):
                return '```{}\n{}\n```\n'.format(self.language, self.code)


class MarkdownFrontMatter(MarkdownComponent):

    def __init__(self, frontmatter):
        self.frontmatter = frontmatter

    def render(self):
         return '---\n{}\n---\n'.format(self.frontmatter)


class MarkdownTable(MarkdownComponent):

    def __init__(self, headers, rows):
        self.headers = headers
        self.rows = rows

    def render(self):
        table = '|' + '|'.join(self.headers) + '|\n'
        table += '|' + '|'.join(['---' for _ in self.headers]) + '|\n'
        for row in self.rows:
            table += '|' + '|'.join(row) + '|\n'
        return table


class MarkdownList(MarkdownComponent):

    def __init__(self, items):
        self.items = items

    def render(self):
        return '\n'.join(['- {}'.format(i) for i in self.items]) + '\n'


class MarkdownOrderedList(MarkdownComponent):

    def __init__(self, items):
        self.items = items

    def render(self):
        return '\n'.join(['{}. {}'.format(i + 1, item) for i, item in enumerate(self.items)]) + '\n'


class MarkdownLink(MarkdownComponent):

    def __init__(self, text, url):
        self.text = text
        self.url = url

    def render(self):
        return '[{}]({})'.format(self.text, self.url)


class MarkdownImage(MarkdownComponent):

        def __init__(self, alt, url):
            self.alt = alt
            self.url = url

        def render(self):
            return '![{}]({})'.format(self.alt, self.url)


class MarkdownHeading(MarkdownComponent):

        def __init__(self, text, level=1):
            self.text = text
            self.level = level

        def render(self):
            return '{} {}\n'.format('#'*self.level, self.text)


class MarkdownHorizontalRule(MarkdownComponent):

        def render(self):
            return '---\n'


class MarkdownBlockquote(MarkdownComponent):

        def __init__(self, text):
            self.text = text

        def render(self):
            return '> {}\n'.format(self.text)


class MarkdownBold(MarkdownComponent):

    def __init__(self, text):
        self.text = text

    def render(self):
        return '**{}**'.format(self.text)


class MarkdownItalic(MarkdownComponent):

    def __init__(self, text):
        self.text = text

    def render(self):
        return '*{}*'.format(self.text)


'''
Block, as know as 内容块, is a special block element, wrapped by three or more `/`. The syntax is as follows:
'''
class MarkdownBlock(MarkdownComponent):

    def __init__(self, name, argument, text, level=3, options=None):
        if options is None:
            options = {}
        self.name = name
        self.argument = argument
        self.text = text
        self.level = level
        self.options = options

    def render(self):
        block = '{} {}{}\n'.format('/'*self.level, self.name, ' | ' + self.argument if self.argument else '')
        for key, value in self.options.items():
            block += '    {}: {}\n'.format(key, value)
        block += '{}\n{}\n'.format(self.text, '/'*self.level)
        return block


class MarkdownAdmonition(MarkdownBlock):

        def __init__(self, title, text, type='note', detail=False, level=3, options=None):
            super().__init__('{}{}'.format('details-' if detail else '', type), title, text, level, options)

        def render(self):
            return super().render()


class MarkdownHtmlBlock(MarkdownBlock):

        def __init__(self, tag, text, level=3, options=None):
            super().__init__('html', tag, text, level, options)

        def render(self):
            return super().render()


class MarkdownTab(MarkdownBlock):

        def __init__(self, title, text, level=3, options=None):
            super().__init__('tab', title, text, level, options)

        def render(self):
            return super().render()


class MarkdownDefinitionList(MarkdownBlock):

    def __init__(self, definitionList=None, level=3, options=None):
        if definitionList is None:
            definitionList = {}
        text = ''
        for key, value in definitionList.items():
            text += '{}\n\n- {}\n\n'.format(key, value)
        super().__init__('define', '', text, level, options)

    def render(self):
        return super().render()


class MarkdownAnnotation(MarkdownComponent):

    def __init__(self, paragraph, texts):
        self.paragraph = paragraph
        self.texts = texts

    def render(self):
        return '{}\n{{.annotate}}\n\n'.format(self.paragraph) + MarkdownOrderedList(self.texts).render()



class MarkdownSymbol(MarkdownComponent):

    def __init__(self, symbol, text=''):
        self.symbol = symbol
        self.text = text

    def render(self):
        return '<!-- md:{}{} -->'.format(self.symbol, ' ' + self.text if self.text else '')


class MarkdownWriter(object):

    def __init__(self):
        self.markdown = Markdown()

    def addLineBreak(self):
        self.markdown.addComponent(MarkdownText('\n'))

    def addText(self, text):
        self.markdown.addComponent(MarkdownText(text))

    def addCodeBlock(self, code, language=None):
        self.markdown.addComponent(MarkdownCodeBlock(code, language))

    def addFrontMatter(self, frontmatter):
        self.markdown.addComponent(MarkdownFrontMatter(frontmatter))

    def addTable(self, headers, rows):
        self.markdown.addComponent(MarkdownTable(headers, rows))

    def addList(self, items):
        self.markdown.addComponent(MarkdownList(items))

    def addOrderedList(self, items):
        self.markdown.addComponent(MarkdownOrderedList(items))

    def addLink(self, text, url):
        self.markdown.addComponent(MarkdownLink(text, url))

    def addImage(self, alt, url):
        self.markdown.addComponent(MarkdownImage(alt, url))

    def addHeading(self, text, level=1):
        self.markdown.addComponent(MarkdownHeading(text, level))

    def addHorizontalRule(self):
        self.markdown.addComponent(MarkdownHorizontalRule())

    def addBlockquote(self, text):
        self.markdown.addComponent(MarkdownBlockquote(text))

    def addBold(self, text):
        self.markdown.addComponent(MarkdownBold(text))

    def addItalic(self, text):
        self.markdown.addComponent(MarkdownItalic(text))

    def addBlock(self, name, argument, text, level=3, options=None):
        self.markdown.addComponent(MarkdownBlock(name, argument, text, level, options))

    def addAdmonition(self, title, text, type='note', detail=False, level=3, options=None):
        self.markdown.addComponent(MarkdownAdmonition(title, text, type, detail, level, options))

    def addHtmlBlock(self, tag, text, level=3, options=None):
        self.markdown.addComponent(MarkdownHtmlBlock(tag, text, level, options))

    def addTab(self, title, text, level=3, options=None):
        self.markdown.addComponent(MarkdownTab(title, text, level, options))

    def addDefinitionList(self, definitionList=None, level=3, options=None):
        self.markdown.addComponent(MarkdownDefinitionList(definitionList, level, options))

    def addAnnotation(self, component, texts):
        self.markdown.addComponent(MarkdownAnnotation(component, texts))

    def addSymbol(self, symbol, text=''):
        self.markdown.addComponent(MarkdownSymbol(symbol, text))

    def preRender(self):
        pass

    def render(self):
        self.preRender()
        return self.markdown.render()
