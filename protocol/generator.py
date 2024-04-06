import json
import os
import re
from bs4 import BeautifulSoup

import pygraphviz as pgv

from protocol.builder import ProtocolBuilder, specialTypeReplace


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
        enums = {}
        with open(r'assets/protocols/html/enums.html', 'r') as f:
            soup = BeautifulSoup(f.read().replace('<uint32_t>', '&lt;uint32_t&gt;'), 'html.parser')
            for row in soup.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == 0:
                    continue
                enums[cells[0].text] = {}
                for cell in cells[1].get_text('\n').split('\n'):
                    if cell:
                        enums[cells[0].text][cell.split(' = ')[0]] = cell.split(' = ')[1]
        for dot in self.dots:
            dotName = dot.replace('.dot', '')
            dotPath = dotName.replace(' ', '_').lower()
            if dotName.endswith('Packet'):
                with open(r'build/protocols/packets/{}.md'.format(dotPath), 'w', encoding="utf-8") as f:
                    builder = ProtocolBuilder(dot, self.dots[dot], enums)
                    f.write(builder.render())
                    dotName = specialTypeReplace(builder.protocol.name).replace('<', '&lt;').replace('>', '&gt;')
                packetPageList.append({'name': dotName, 'path': 'refs/protocols/packets/{}.md'.format(dotPath)})
            else:
                with open(r'build/protocols/types/{}.md'.format(dotPath), 'w', encoding="utf-8") as f:
                    builder = ProtocolBuilder(dot, self.dots[dot], enums)
                    f.write(builder.render())
                    dotName = specialTypeReplace(builder.protocol.name).replace('<', '&lt;').replace('>', '&gt;')
                typePageList.append({'name': dotName, 'path': 'refs/protocols/types/{}.md'.format(dotPath)})
        packetPageListText = '\n'.join(['- <samp>{}</samp>: {}'.format(p['name'], p['path']) for p in packetPageList])
        typePageListText = '\n'.join(['- <samp>{}</samp>: {}'.format(p['name'], p['path']) for p in typePageList])
        return packetPageListText, typePageListText
