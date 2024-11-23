import json
import os
import re

from script.builder import ModuleBuilder, ClassBuilder, InterfaceBuilder, EnumBuilder, TypeAliasBuilder, ErrorBuilder


class ScriptAPIGenerator(object):
    def __init__(self):
        self.module = {}
        with open(r'assets/docs/script_modules/mojang-minecraft_0.1.0.json', 'r') as f:
            self.module["server"] = {}
            self.module["server"]["0.1.0"] = json.loads(f.read())
        with open(r'assets/docs/script_modules/mojang-minecraft-ui_0.1.0.json', 'r') as f:
            self.module["server-ui"] = {}
            self.module["server-ui"]["0.1.0"] = json.loads(f.read())
        for root, dirs, files in os.walk(r'assets/docs/script_modules/@minecraft'):
            for file in files:
                with open(os.path.join(root, file), 'r') as f:
                    name, version = re.match(r'(.*)_(.*).json', file).groups()
                    if re.match(r'.*?-alpha', version):
                        version = 'alpha'
                    if re.match(r'.*?-beta', version):
                        version = 'beta'
                    if re.match(r'.*?-internal', version):
                        version = 'internal'
                    if name not in self.module:
                        self.module[name] = {}
                    self.module[name][version] = json.loads(f.read())
        for name in self.module:
            keys = list(self.module[name].keys())
            keys.sort(key=lambda x: (
                3 if x == 'alpha' else
                2 if x == 'internal' else
                1 if x == 'beta' else
                0,
                tuple(int(part) for part in x.split('.')) if x not in ['alpha', 'internal', 'beta'] else ()
            ))
            keys.reverse()
            self.module[name] = {k: self.module[name][k] for k in keys}

    def generate(self):
        if not os.path.exists(r'build'):
            os.mkdir(r'build')
        if not os.path.exists(r'build/script-api'):
            os.mkdir(r'build/script-api')
        pageListText = ''
        for name in self.module:
            if not os.path.exists(r'build/script-api/{}'.format(name)):
                os.mkdir(r'build/script-api/{}'.format(name))
            modulePageListText = ''
            for version in self.module[name]:
                if not os.path.exists(r'build/script-api/{}/{}'.format(name, version)):
                    os.mkdir(r'build/script-api/{}/{}'.format(name, version))
                versionPageListText = ''
                with open(r'build/script-api/{}/{}/index.md'.format(name, version), 'w', encoding="utf-8") as f:
                    builder = ModuleBuilder(self.module[name][version])
                    f.write(builder.render())
                    versionPageListText += '- {}'.format('refs/script-api/{}/{}/index.md'.format(name, version))
                classPageList = []
                if self.module[name][version]['classes']:
                    for class_ in self.module[name][version]['classes']:
                        className = class_['name']
                        classPath = className.replace(' ', '_').lower()
                        with open(r'build/script-api/{}/{}/{}.md'.format(name, version, classPath), 'w', encoding="utf-8") as f:
                            builder = ClassBuilder(class_)
                            f.write(builder.render())
                            classPageList.append({'name': className, 'path': 'refs/script-api/{}/{}/{}.md'.format(name, version, classPath)})
                    classPageListText = '\n'.join(['- <code>{}</code>: {}'.format(p['name'], p['path']) for p in classPageList])
                    versionPageListText += '\n- 类: \n  {}'.format(classPageListText.replace('\n', '\n  '))
                if self.module[name][version]['interfaces']:
                    interfacePageList = []
                    for interface in self.module[name][version]['interfaces']:
                        interfaceName = interface['name']
                        interfacePath = interfaceName.replace(' ', '_').lower()
                        with open(r'build/script-api/{}/{}/{}.md'.format(name, version, interfacePath), 'w', encoding="utf-8") as f:
                            builder = InterfaceBuilder(interface)
                            f.write(builder.render())
                            interfacePageList.append({'name': interfaceName, 'path': 'refs/script-api/{}/{}/{}.md'.format(name, version, interfacePath)})
                    interfacePageListText = '\n'.join(['- <code>{}</code>: {}'.format(p['name'], p['path']) for p in interfacePageList])
                    versionPageListText += '\n- 接口: \n  {}'.format(interfacePageListText.replace('\n', '\n  '))
                if self.module[name][version]['enums']:
                    enumPageList = []
                    for enum in self.module[name][version]['enums']:
                        enumName = enum['name']
                        enumPath = enumName.replace(' ', '_').lower()
                        with open(r'build/script-api/{}/{}/{}.md'.format(name, version, enumPath), 'w', encoding="utf-8") as f:
                            builder = EnumBuilder(enum)
                            f.write(builder.render())
                            enumPageList.append({'name': enumName, 'path': 'refs/script-api/{}/{}/{}.md'.format(name, version, enumPath)})
                    enumPageListText = '\n'.join(['- <code>{}</code>: {}'.format(p['name'], p['path']) for p in enumPageList])
                    versionPageListText += '\n- 枚举: \n  {}'.format(enumPageListText.replace('\n', '\n  '))
                if self.module[name][version]['type_aliases']:
                    typeAliasPageList = []
                    for typeAlias in self.module[name][version]['type_aliases']:
                        typeAliasName = typeAlias['name']
                        typeAliasPath = typeAliasName.replace(' ', '_').lower()
                        with open(r'build/script-api/{}/{}/{}.md'.format(name, version, typeAliasPath), 'w', encoding="utf-8") as f:
                            builder = TypeAliasBuilder(typeAlias)
                            f.write(builder.render())
                            typeAliasPageList.append({'name': typeAliasName, 'path': 'refs/script-api/{}/{}/{}.md'.format(name, version, typeAliasPath)})
                    typeAliasPageListText = '\n'.join(['- <code>{}</code>: {}'.format(p['name'], p['path']) for p in typeAliasPageList])
                    versionPageListText += '\n- 类型别名: \n  {}'.format(typeAliasPageListText.replace('\n', '\n  '))
                if self.module[name][version]['errors']:
                    errorPageList = []
                    for error in self.module[name][version]['errors']:
                        errorName = error['name']
                        errorPath = errorName.replace(' ', '_').lower()
                        with open(r'build/script-api/{}/{}/{}.md'.format(name, version, errorPath), 'w', encoding="utf-8") as f:
                            builder = ErrorBuilder(error)
                            f.write(builder.render())
                            errorPageList.append({'name': errorName, 'path': 'refs/script-api/{}/{}/{}.md'.format(name, version, errorPath)})
                    errorPageListText = '\n'.join(['- <code>{}</code>: {}'.format(p['name'], p['path']) for p in errorPageList])
                    versionPageListText += '\n- 错误: \n  {}'.format(errorPageListText.replace('\n', '\n  '))
                modulePageListText += '\n- <code>{}</code>: \n  {}'.format(version, versionPageListText.replace('\n', '\n  '))
            pageListText += '\n- <code>@minecraft/{}</code>:   {}'.format(name, modulePageListText.replace('\n', '\n  '))
        return pageListText