import os

import pygraphviz as pgv
from markdown.writer import *

import ast


class ProtocolBuilder(MarkdownWriter):

    def __init__(self, protocol=None, enums=None):
        super().__init__()
        if enums is None:
            enums = {}
        if protocol is None:
            protocol = {}
        self.protocol = pgv.AGraph(os.path.join(r'assets/protocols/dot', protocol))
        self.enums = enums

    def preRender(self):
        version = 'r/20_u7'
        protocolVersion = 662
        protocolName = MarkdownSymbol('samp', self.protocol.name).render()
        self.addHeading(protocolName, 1)
        self.addBlockquote('文档版本：{}<br/>协议版本：{}'.format(version, protocolVersion))
        if self.protocol.name.endswith('Packet'):
            fileType = '数据包'
        else:
            fileType = '类型'
        packetId = parseComment(self.protocol.nodes()[0])["branchId"]
        self.addText('{}{}{}{}。'.format(protocolName, fileType, '', f'，数字ID是`{packetId}`' if packetId else ''))  #todo add packet description
        self.addHeading('结构', 2)
        self.addText('```dot\n{}\n```'.format(self.protocol.to_string()))
        self.addHeading('字段', 2)
        defList = {}
        edges = self.protocol.edges()
        buildDefList(defList, edges, self.protocol.nodes()[0])
        self.addDefinitionList(defList)

    def render(self):
        return super().render()


'''comment="name: \"CompoundTag\", typeName: \"\", id: 0, branchId: 0, recurseId: -1, attributes: 0, notes: \"\""'''
def parseComment(protocolNode: str) -> dict:
    comment = protocolNode.attr["comment"].replace("name", "'name'").replace("typeName", "'typeName'").replace("id", "'id'").replace("branchId", "'branchId'").replace("recurseId", "'recurseId'").replace("attributes", "'attributes'").replace("notes", "'notes'")
    return ast.literal_eval(f'{{{comment}}}')


def buildDefList(defList, edges, node):
    comment = parseComment(node)
    outs = []
    description = ''
    for edge in edges:
        if edge[0] == node:
            if edge[1] not in defList:
                outs.append(edge[1])
                edges.remove(edge)
    if comment["attributes"] == 2:
        defList['{}'.format(node.attr["label"])] = ''
        writer = MarkdownWriter()
        for out in outs:
            if parseComment(out)["attributes"] == 4:
                subDefList = {}
                buildDefList(subDefList, edges, out)
                writer.addTab('{}'.format(out.attr["label"]), MarkdownDefinitionList(subDefList).render())
        defList[writer.render()] = ''
    elif comment["attributes"] == 8:
        defList['{}'.format(node.attr["label"])] = ''
        for out in outs:
            if parseComment(out)["attributes"] == 16:
                if out.attr["label"] == 'example element':
                    out.attr["label"] = '{}的示例元素'.format(node.attr["label"])
                buildDefList(defList, edges, out)
            else:
                if out.attr["label"] == 'Array Size':
                    out.attr["label"] = '{}数组的大小'.format(node.attr["label"])
                buildDefList(defList, edges, out)
    elif len(outs) == 1:
        if parseComment(outs[0])["attributes"] == 512:
            type = outs[0].attr["label"]
            if comment["attributes"] == 256:
                typeLink = MarkdownLink(MarkdownSymbol('samp', type).render(), 'refs/protocols/types/{}.md'.format(type))
            else:
                typeLink = MarkdownSymbol('samp', type).render()
            defList['{}：{}'.format(node.attr["label"], typeLink)] = description
        else:
            defList['{}'.format(node.attr["label"])] = ''
            buildDefList(defList, edges, outs[0])
    elif len(outs) > 1:
        for out in outs:
            defList['{}'.format(node.attr["label"])] = ''
            buildDefList(defList, edges, out)