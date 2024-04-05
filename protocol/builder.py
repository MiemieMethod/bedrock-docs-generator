import os
import re

import pygraphviz as pgv
from markdown.writer import *

import ast


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
        protocolName = MarkdownSymbol('samp', self.protocol.name.replace('<', '&lt;').replace('>', '&gt;')).render()
        self.addHeading(protocolName, 1)
        self.addBlockquote('文档版本：{}<br/>协议版本：{}'.format(version, protocolVersion))
        if self.protocol.name.endswith('Packet'):
            fileType = '数据包'
        else:
            fileType = '类型'
        packetId = parseComment(self.protocol.nodes()[0])["branchId"]
        self.addText('{}{}{}{}。'.format(protocolName, fileType, '', f'，数字ID是`{packetId}`' if packetId else ''))  #todo add packet description
        self.addHeading('结构', 2)
        self.addText('```viz\n{}\n```'.format(self.protocolFile))
        self.addHeading('字段', 2)
        # defList = {}
        # buildDefList(defList, self.protocol, self.protocol.nodes()[0])
        # self.addDefinitionList(defList)
        self.addText(buildCodeAndResult(self.protocol, self.protocol.nodes()[0]))

    def render(self):
        return super().render()


'''comment="name: \"CompoundTag\", typeName: \"\", id: 0, branchId: 0, recurseId: -1, attributes: 0, notes: \"\""'''
def parseComment(protocolNode: str) -> dict:
    comment = protocolNode.attr["comment"].replace("name", "'name'").replace("typeName", "'typeName'").replace("id", "'id'").replace("branchId", "'branchId'").replace("recurseId", "'recurseId'").replace("attributes", "'attributes'").replace("notes", "'notes'")
    return ast.literal_eval(f'{{{comment}}}')


def buildDefList(defList, protocol, node, level=3):

    comment = parseComment(node)
    outs = []
    description = ''
    edges = protocol.edges(node)
    if node.attr["label"] == 'ActorEventPacket':
        print(protocol.edges(node))
    for edge in edges:
        if edge[0] == node:
            outs.append(edge[1])
    if comment["attributes"] == 2:
        defList['{}'.format(node.attr["label"])] = ''
        writer = MarkdownWriter()
        for out in outs:
            if parseComment(out)["attributes"] == 4:
                subDefList = {}
                buildDefList(subDefList, protocol, out, level + 2)
                writer.addTab('{}'.format(out.attr["label"]), MarkdownDefinitionList(subDefList, level + 2).render(), level + 1)
        defList[writer.render()] = ''
    elif comment["attributes"] == 8:
        defList['{}'.format(node.attr["label"])] = ''
        for out in outs:
            if parseComment(out)["attributes"] == 16:
                if out.attr["label"] == 'example element':
                    out.attr["label"] = '{}的示例元素'.format(node.attr["label"])
                subDefList = {}
                buildDefList(subDefList, protocol, out, level + 1)
                defList['{}'.format(MarkdownDefinitionList(subDefList, level + 1).render())] = ''
            else:
                if out.attr["label"] == 'Array Size':
                    out.attr["label"] = '{}数组的大小'.format(node.attr["label"])
                subDefList = {}
                buildDefList(subDefList, protocol, out, level + 1)
                defList['{}'.format(MarkdownDefinitionList(subDefList, level + 1).render())] = ''
    elif len(outs) == 1:
        if parseComment(outs[0])["attributes"] == 512:
            type = outs[0].attr["label"]
            if comment["attributes"] == 256:
                typeLink = MarkdownLink(MarkdownSymbol('samp', type).render(), '../types/{}.md'.format(type.replace(' ', '_').lower())).render()
            else:
                typeLink = MarkdownSymbol('samp', type).render()
            description = '类型：{}。{}'.format(type, comment["notes"])
            defList['{}：{}'.format(node.attr["label"], typeLink)] = description
        else:
            defList['{}'.format(node.attr["label"])] = ''
            buildDefList(defList, protocol, outs[0], level)
    elif len(outs) > 1:
        defList['{}'.format(node.attr["label"])] = ''
        for out in outs:
            if node.attr["label"] == 'ActorEventPacket':
                print(out.attr["label"])
            buildDefList(defList, protocol, out, level)


def buildCodeAndResult(protocol, node, level=3):
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
        if comment["attributes"] == 256:
            typeLink = MarkdownLink(MarkdownSymbol('samp', type).render(), '../types/{}.md'.format(re.sub(r"[ :<>]", r"_", type).lower())).render()
        else:
            typeLink = MarkdownSymbol('samp', type).render()
        description = '{}。{}'.format('类型：' + MarkdownSymbol('samp', type).render() if type != '[No Data]' else '无数据', comment["notes"])
        defList['{}：{}'.format(node.attr["label"], typeLink)] = description
        writer.addDefinitionList(defList, level)
    elif comment["attributes"] == 2:
        writer.addBlockquote(re.sub(r"Dependency on '(.*)'", r"依赖于`\1`", node.attr["label"]))
        for out in outs:
            tabLabel = re.sub(r"if \((.*)\)", r"{}如果为`\1`".format(re.sub(r"Dependency on '(.*)'", r"`\1`", node.attr["label"])), out.attr["label"])
            if parseComment(out)["attributes"] == 4:
                content = buildCodeAndResult(protocol, out, level + 2)
                writer.addTab('{}'.format(tabLabel), content, level + 1)
    else:
        binArray = ''
        for out in outs:
            binArray += '[{}]'.format(out.attr["label"].replace(' ', '_').lower().replace('example_element', '[example_element]..'))
        if comment["attributes"] == 8:
            for out in outs:
                if parseComment(out)["attributes"] == 16:
                    if out.attr["label"] == 'example element':
                        out.attr["label"] = '示例元素'
                else:
                    if out.attr["label"] == 'Array Size':
                        out.attr["label"] = '数组大小'
        writer.addCodeBlock(binArray, "title='{}'".format(node.attr["label"]))
        content = ''
        for out in outs:
            content += buildCodeAndResult(protocol, out, level + 1)
        writer.addHtmlBlock('div.result', content, level)
    return writer.render()