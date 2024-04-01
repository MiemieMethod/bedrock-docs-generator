from markdown.writer import *



class ItemTagBuilder(MarkdownWriter):

    def __init__(self, tags):
        super().__init__()
        self.tags = tags

    def preRender(self):
        version = '1.20.72.01'
        self.addHeading('原版物品标签', 1)
        self.addBlockquote('文档版本：{}'.format(version))
        self.addAdmonition('描述', '[物品标签]是一种用于标记物品的字符串。它们可以用于选择性地标记物品，以便在别处引用它们。当前页面给出了物品标签的原版使用情况。\n\n  [物品标签]: ../../../../docs/items/tags.md', 'abstract')
        self.addTable(['物品标签', '原版使用物品'], [[f'`{tag}`', '`' + '`<br/>`'.join(self.tags[tag]) + '`' if len(self.tags[tag]) >= 1 else '无'] for tag in self.tags])

    def render(self):
        return super().render()