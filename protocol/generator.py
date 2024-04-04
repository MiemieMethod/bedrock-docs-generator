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
                        self.dots[file] = re.sub(r"(\n[^0-9r{}\n])", r"<br/>", self.dots[file])
                        self.dots[file] = re.sub(r"(\n[^0-9r{}\n])", r"<br/>", self.dots[file])
                        f.write(self.dots[file])


    def generate(self):
        if not os.path.exists(r'build/protocols'):
            os.mkdir(r'build/protocols')
        if not os.path.exists(r'build/protocols/packets'):
            os.mkdir(r'build/protocols/packets')
        for dot in self.dots:
            with open(r'build/protocols/packets/{}.md'.format(dot.replace('.dot', '')), 'w', encoding="utf-8") as f:
                f.write(ProtocolBuilder(dot, self.dots[dot]).render())
        return ''
