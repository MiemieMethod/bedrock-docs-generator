from markdown.writer import *


class CommandBuilder(MarkdownWriter):

    def __init__(self, command=None, enums=None, enumsMap=None):
        super().__init__()
        if enumsMap is None:
            enumsMap = {}
        if enums is None:
            enums = {}
        if command is None:
            command = {}
        self.command = command
        self.enums = enums
        self.enumsMap = enumsMap

    def preRender(self):
        version = '1.20.80.24'
        permissionLevel = [
            'any',
            'gamedirectors',
            'admin',
            'host',
            'owner',
            'internal'
        ]
        self.addHeading('`/{}`'.format(self.command["name"]), 1)
        self.addBlockquote('文档版本：{}'.format(version))
        self.addText('`/{}`命令{}'.format(self.command["name"], self.command["description"]))
        self.addAdmonition('执行条件', '该命令需要权限等级：`{}`|`{}`。{}'.format(permissionLevel[self.command["permission_level"]], self.command["permission_level"], '该命令需要开启作弊。' if self.command["requires_cheats"] else ''), 'settings')
        if self.command["aliases"]:
            self.addAdmonition('别名', '该命令还可以使用以下别名：`{}`。'.format('`、`'.join(['/' + a["name"] for a in self.command["aliases"]])), 'info')
        self.addHeading('用法', 2)
        for overload in self.command["overloads"]:
            writer = MarkdownWriter()
            paramsWriter = MarkdownWriter()
            defList = {}
            description = '/{}'.format(self.command["name"])
            for param in overload["params"]:
                descriptorDict = self.enumsMap.get(param["type"]["name"], self.enums.get(param["type"]["name"], {}))
                descriptor = descriptorDict.get('description', descriptorDict.get('name', param["type"]["name"]))
                descriptor = 'l' if param["type"]["name"] == 'postfix_l' else descriptor
                enumList = self.enums.get(descriptor.upper(), {}).get('values', None)

                dataType = '基本类型'
                enumTableText = ''

                if isinstance(enumList, list) and len(enumList) == 1:
                    description += ' {}'.format(enumList[0]['value'])
                elif isinstance(enumList, list) and len(enumList) == 0:
                    description += ' {}{}:string{}'.format('[' if param["is_optional"] else '<', param["name"], ']' if param["is_optional"] else '>')

                    dataType = '软枚举类型'
                elif param["type"]["name"] == 'postfix_l':
                    description += ' {}{}:int{}L'.format('[' if param["is_optional"] else '<', param["name"], ']' if param["is_optional"] else '>')

                    enumTableText = '后缀为`L`。'
                    dataType = '后缀类型'
                else:
                    description += ' {}{}:{}{}'.format('[' if param["is_optional"] else '<', param["name"], descriptor, ']' if param["is_optional"] else '>')

                if isinstance(enumList, list) and len(enumList) >= 1:
                    enumTable = MarkdownTable(['值', '描述'], [['`{}`'.format(e['value']), ''] for e in enumList])  # todo: add enum description
                    enumTableText = '枚举值如下：\n\n' + enumTable.render() if len(enumList) > 1 else '单值枚举，请直接使用`{}`。'.format(enumList[0]['value'])
                    dataType = '枚举类型'

                defList['`{}`: {}'.format(param["name"], MarkdownSymbol('samp', descriptor).render())] = '{}。{}'.format(dataType, enumTableText)  # todo: add param description
            writer.addCodeBlock(description, 'mcfunction')
            if overload.get("version", [1, -1]) != [1, -1]:
                paramsWriter.addSymbol('version command', '{} {} true true'.format(overload["version"][0] if overload["version"][0] != 1 else '*', overload["version"][1] if overload["version"][1] != -1 else '*'))
            paramsWriter.addDefinitionList(defList, 5)
            writer.addHtmlBlock('div.result', paramsWriter.render(), 4)
            self.addTab('重载{}'.format(overload["name"]), writer.render())

    def render(self):
        return super().render()

