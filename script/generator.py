import json
import os
import re

from script.builder import ClassBuilder, InterfaceBuilder, EnumBuilder


class ScriptAPIGenerator(object):
    def __init__(self):
        self.module = {}
        with open(r'assets/docs/script_modules/@minecraft/server_1.12.0-beta.json', 'r') as f:
            self.module = json.loads(f.read())

    def generate(self):
        if not os.path.exists(r'build/script-api'):
            os.mkdir(r'build/script-api')
        if not os.path.exists(r'build/script-api/server'):
            os.mkdir(r'build/script-api/server')
        if not os.path.exists(r'build/script-api/server/beta'):
            os.mkdir(r'build/script-api/server/beta')
        classPageList = []
        for class_ in self.module['classes']:
            className = class_['name']
            classPath = className.replace(' ', '_').lower()
            with open(r'build/script-api/server/beta/{}.md'.format(classPath), 'w', encoding="utf-8") as f:
                builder = ClassBuilder(class_)
                f.write(builder.render())
                classPageList.append({'name': className, 'path': 'refs/script-api/server/beta/{}.md'.format(classPath)})
        classPageListText = '\n'.join(['- <samp>{}</samp>: {}'.format(p['name'], p['path']) for p in classPageList])
        interfacePageList = []
        for interface in self.module['interfaces']:
            interfaceName = interface['name']
            interfacePath = interfaceName.replace(' ', '_').lower()
            with open(r'build/script-api/server/beta/{}.md'.format(interfacePath), 'w', encoding="utf-8") as f:
                builder = InterfaceBuilder(interface)
                f.write(builder.render())
                interfacePageList.append({'name': interfaceName, 'path': 'refs/script-api/server/beta/{}.md'.format(interfacePath)})
        interfacePageListText = '\n'.join(['- <samp>{}</samp>: {}'.format(p['name'], p['path']) for p in interfacePageList])
        enumPageList = []
        for enum in self.module['enums']:
            enumName = enum['name']
            enumPath = enumName.replace(' ', '_').lower()
            with open(r'build/script-api/server/beta/{}.md'.format(enumPath), 'w', encoding="utf-8") as f:
                builder = EnumBuilder(enum)
                f.write(builder.render())
                enumPageList.append({'name': enumName, 'path': 'refs/script-api/server/beta/{}.md'.format(enumPath)})
        enumPageListText = '\n'.join(['- <samp>{}</samp>: {}'.format(p['name'], p['path']) for p in enumPageList])
        pageListText = '- 类: \n  {}\n- 接口: \n  {}\n- 枚举: \n  {}'.format(classPageListText.replace('\n', '\n  '), interfacePageListText.replace('\n', '\n  '), enumPageListText.replace('\n', '\n  '))
        return pageListText