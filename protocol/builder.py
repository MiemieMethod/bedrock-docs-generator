import os
import re

import pygraphviz as pgv
from markdown.writer import *

import ast

from translation.i18n import i18n


class ProtocolBuilder(MarkdownWriter):

    def __init__(self, protocol=None, protocolFile = '', enums=None):
        super().__init__()
        if enums is None:
            enums = {}
        if protocol is None:
            protocol = {}
        self.protocol = pgv.AGraph(os.path.join(r'assets/protocols/dot', protocol))
        self.protocolFile = protocolFile
        self.enums = enums

    def preRender(self):
        version = 'r/20_u7'
        protocolVersion = 662
        protocolName = MarkdownSymbol('samp', specialTypeReplace(self.protocol.name).replace('<', '&lt;').replace('>', '&gt;')).render()
        self.addHeading(protocolName, 1)
        self.addBlockquote('文档版本：{}<br/>协议版本：{}'.format(version, protocolVersion))
        if self.protocol.name.endswith('Packet'):
            fileType = '数据包'
        else:
            fileType = '类型'
        packetId = parseComment(self.protocol.nodes()[0])["branchId"]
        self.addText('{}{}{}{}。该{}用于{}'.format(protocolName, fileType, '', f'，数字ID是`{packetId}`' if packetId else '', fileType, i18n.get(f'protocol.{'packet' if packetId else 'type'}.{specialTypeReplace(self.protocol.name).replace(' ', '_').lower()}.description')))
        self.addHeading('结构', 2)
        self.addText('```viz\n{}\n```'.format(self.protocolFile))
        self.addHeading('字段', 2)
        self.addText(buildCodeAndResult(self.protocol, self.enums, self.protocol.nodes()[0]))

    def render(self):
        return super().render()


'''comment="name: \"CompoundTag\", typeName: \"\", id: 0, branchId: 0, recurseId: -1, attributes: 0, notes: \"\""'''
def parseComment(protocolNode: str) -> dict:
    comment = protocolNode.attr["comment"].replace("name", "'name'").replace("typeName", "'typeName'").replace("id", "'id'").replace("branchId", "'branchId'").replace("recurseId", "'recurseId'").replace("attributes", "'attributes'").replace("notes", "'notes'")
    return ast.literal_eval(f'{{{comment}}}')

def specialTypeReplace(type):
    if type == 'std::vector<class std::unique_ptr<class DataItem,struct std::default_delete<class DataItem> >,class std::allocator<class std::unique_ptr<class DataItem,struct std::default_delete<class DataItem> > > >':
        return 'std::vector<std::unique_ptr<DataItem>>'
    elif type == 'std::optional<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >':
        return 'std::optional<std::string>'
    elif type == 'String':
        return 'string'
    elif type == 'Fixed Float':
        return 'fixed float'
    else:
        return type


def buildCodeAndResult(protocol, enums, node, level=3):
    comment = parseComment(node)
    outs = []
    edges = protocol.edges(node)
    for edge in edges:
        if edge[0] == node:
            outs.append(edge[1])
    writer = MarkdownWriter()
    if len(outs) == 1 and parseComment(outs[0])["attributes"] == 512:
        defList = {}
        type = outs[0].attr["label"]
        path = type
        type = specialTypeReplace(type)
        typeToShow = type.replace('<', '&lt;').replace('>', '&gt;')
        typeName = '基本类型'
        if comment["attributes"] == 256 or type == 'string' or type == 'fixed float':
            typeLink = MarkdownLink(MarkdownSymbol('samp', typeToShow).render(), '../types/{}.md'.format(re.sub(r"[ :<>]", r"_", path)[0:127].lower())).render()
            typeName = '特殊类型'
        else:
            typeLink = MarkdownSymbol('samp', typeToShow).render()
        enumTables = ''
        enumList = re.findall(r"^enumeration: (.*)", comment["notes"])
        for enum in enumList:
            enumTables += MarkdownTable(['键', '值', '描述'], [[f'`{k}`', f'`{v}`', i18n.get(f'protocol.enum.{k.lower()}')] for k, v in enums[enum].items()]).render(1)
        enumList = re.findall(r"^Available ones: (.*)", comment["notes"])
        for enum in enumList:
            values = enum.split(', ')
            enumTables += MarkdownTable(['值', '描述'], [[f'`{v}`', i18n.get(f'protocol.enum.{v.lower()}')] for v in values]).render(1)
        comment["notes"] = re.sub(r"^enumeration: (.*)", r"", comment["notes"])
        comment["notes"] = re.sub(r"^Available ones: (.*)", r"", comment["notes"])
        description = '{}{}{}'.format(typeName + ('枚举' if enumTables else '') + '。' + i18n.get(f'protocol.{'packet' if parseComment(protocol.nodes()[0])["branchId"] else 'type'}.{specialTypeReplace(protocol.name).replace(' ', '_').lower()}.{formatBinArrayItem(node.attr["label"])}.description') if type != '[No Data]' else '无数据', comment["notes"], '枚举值如下：\n\n' + enumTables if enumTables else '')
        defList['{}：{}'.format(node.attr["label"], typeLink)] = description
        writer.addDefinitionList(defList, level)
    elif comment["attributes"] == 2:
        writer.addBlockquote(re.sub(r"Dependency on '(.*)'", r"依赖于`\1`", node.attr["label"]))
        for out in outs:
            tabLabel = re.sub(r"if \((.*)\)", r"{}如果为`\1`".format(re.sub(r"Dependency on '(.*)'", r"`\1`", node.attr["label"])), out.attr["label"])
            if parseComment(out)["attributes"] == 4:
                content = buildCodeAndResult(protocol, enums, out, level + 2)
                writer.addTab('{}'.format(tabLabel), content, level + 1)
    else:
        binArray = ''
        for out in outs:
            binArray += '[{}]'.format(formatBinArrayItem(out.attr["label"]))
        if comment["attributes"] == 8:
            for out in outs:
                if parseComment(out)["attributes"] == 16:
                    if out.attr["label"] == 'example element':
                        out.attr["label"] = '示例元素'
                else:
                    if out.attr["label"] == 'Array Size':
                        out.attr["label"] = '数组大小'
        writer.addCodeBlock(binArray, "title='{}'".format(specialTypeReplace(node.attr["label"]).replace('<', '&lt;').replace('>', '&gt;')))
        content = ''
        for out in outs:
            content += buildCodeAndResult(protocol, enums, out, level + 1)
        writer.addHtmlBlock('div.result', content, level)
    return writer.render()

def formatBinArrayItem(item):
    return re.sub(r" \((.*?)\)", r"", item).replace(' - ', ' ').replace("'", '').replace(' ?', '').replace('?', '').replace(',', '').replace('==', 'is').replace('<=', 'le').replace('>=', 'ge').replace(' < ', ' l ').replace(' > ', ' g ').replace('||', 'or').replace(' ', '_').lower().replace('example_element', '[example_element]..')