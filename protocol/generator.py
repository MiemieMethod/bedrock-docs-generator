import json
import os
import re


from protocol.builder import ProtocolBuilder


class ProtocolGenerator(object):
    def __init__(self):
        self.dots = {}
        for root, dirs, files in os.walk(r'assets/protocols/dot'):
            for file in files:
                if file.endswith('.dot'):
                    with open(os.path.join(root, file), 'r') as f:
                        self.dots[file] = f.read()
                    with open(os.path.join(root, file), 'w') as f:
                        self.dots[file] = re.sub(r"(\n[^0-9r{}\n])", r" ", self.dots[file])
                        self.dots[file] = re.sub(r"(\n[^0-9r{}\n])", r" ", self.dots[file])
                        f.write(self.dots[file])


    def generate(self):
        packetPageList = []
        typePageList = []
        if not os.path.exists(r'build/protocols'):
            os.mkdir(r'build/protocols')
        if not os.path.exists(r'build/protocols/packets'):
            os.mkdir(r'build/protocols/packets')
        if not os.path.exists(r'build/protocols/types'):
            os.mkdir(r'build/protocols/types')
        for dot in self.dots:
            dotName = dot.replace('.dot', '')
            if dotName.endswith('Packet'):
                with open(r'build/protocols/packets/{}.md'.format(dotName), 'w', encoding="utf-8") as f:
                    f.write(ProtocolBuilder(dot, self.dots[dot]).render())
                packetPageList.append({'name': dotName, 'path': 'refs/protocols/packets/{}.md'.format(dotName)})
            else:
                with open(r'build/protocols/types/{}.md'.format(dotName), 'w', encoding="utf-8") as f:
                    f.write(ProtocolBuilder(dot, self.dots[dot]).render())
                typePageList.append({'name': dotName, 'path': 'refs/protocols/types/{}.md'.format(dotName)})
        packetPageListText = '\n'.join(['- <samp>{}</samp>: {}'.format(p['name'], p['path']) for p in packetPageList])
        typePageListText = '\n'.join(['- <samp>{}</samp>: {}'.format(p['name'], p['path']) for p in typePageList])
        return packetPageListText, typePageListText
