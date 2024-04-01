from markdown.writer import *



class BlockTagBuilder(MarkdownWriter):

    def __init__(self, tags):
        super().__init__()
        self.tags = tags

    def preRender(self):
        version = '1.20.72.01'
        self.addHeading('原版方块标签', 1)
        self.addBlockquote('文档版本：{}'.format(version))
        self.addAdmonition('描述', '[方块标签]是一种用于标记方块的字符串。它们可以用于选择性地标记方块，以便在别处引用它们。当前页面给出了方块标签的原版使用情况。\n\n  [方块标签]: ../../../../docs/blocks/tags.md', 'abstract')
        self.addTable(['方块标签', '原版使用方块'], [[f'`{tag}`', '`' + '`<br/>`'.join(self.tags[tag]) + '`' if len(self.tags[tag]) >= 1 else '无'] for tag in self.tags])

    def render(self):
        return super().render()