import re

from markdown.writer import *
from translation.i18n import i18n


def localizationKey(name, arg=''):
    return i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}{f'.{ModuleBuilder.currentClassName.lower()}' if ModuleBuilder.currentClassName.lower() else ''}.{name.lower()}{f'.{arg.lower()}' if arg else ''}.description') if i18n.contain(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}{f'.{ModuleBuilder.currentClassName.lower()}' if ModuleBuilder.currentClassName.lower() else ''}.{name.lower()}{f'.{arg.lower()}' if arg else ''}.description') else i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}{f'.{ModuleBuilder.currentClassName.lower()}' if ModuleBuilder.currentClassName.lower() else ''}.{name.lower()}{f'.{arg.lower()}' if arg else ''}.description')


class FunctionBuilder(MarkdownWriter):

    def __init__(self, function=None, fromRoot=False):
        super().__init__()
        if function is None:
            function = {}
        self.function = function
        self.fromRoot = fromRoot

    def preRender(self):
        defList = {}
        defList[f'`{self.function["name"]}`'] = ''
        self.addDefinitionList(defList)
        self.addText(localizationKey(self.function["name"]))
        prefix = 'new ' if self.function["is_constructor"] else ('static ' if self.function["is_static"] else '')
        arguments = argumentSignature(self.function["arguments"])
        self.addCodeBlock(f'{prefix}{self.function["name"]}({arguments}): {typeString(self.function["return_type"], True)}', 'js')
        writer = MarkdownWriter()
        if len(self.function["arguments"]) > 0:
            i = 1
            for argument in self.function["arguments"]:
                defList = {}
                description = localizationKey(self.function["name"].lower(), argument["name"])
                i += 1
                defList[f'`{argument["name"]}`：{typeString(argument["type"], True, True, self.fromRoot)}'] = description
                writer.addDefinitionList(defList, 4)
        writer.addDefinitionList({f'返回值：{typeString(self.function["return_type"], True, True, self.fromRoot)}': i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}{f'.{ModuleBuilder.currentClassName.lower()}' if ModuleBuilder.currentClassName.lower() else ''}.{self.function["name"].lower()}.return') if i18n.contain(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}{f'.{ModuleBuilder.currentClassName.lower()}' if ModuleBuilder.currentClassName.lower() else ''}.{self.function["name"].lower()}.return') else i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}{f'.{ModuleBuilder.currentClassName.lower()}' if ModuleBuilder.currentClassName.lower() else ''}.{self.function["name"].lower()}.return')}, 4)
        self.addHtmlBlock('div.result', writer.render())

    def render(self):
        return super().render()



class PropertyBuilder(MarkdownWriter):

    def __init__(self, property_=None, fromRoot=False):
        super().__init__()
        if property_ is None:
            property_ = {}
        self.property_ = property_
        self.fromRoot = fromRoot

    def preRender(self):
        defList = {}
        defList[f'`{self.property_["name"]}`'] = ''
        self.addDefinitionList(defList)
        prefix = 'static ' if self.property_.get('is_static', '') else ''
        prefix += 'read-only ' if self.property_["is_read_only"] else ''
        self.addCodeBlock(f'{prefix}{self.property_["name"]}: {typeString(self.property_["type"], True)};', 'js')
        writer = MarkdownWriter()
        defList = {}
        defList[f'`{self.property_["name"]}`：{typeString(self.property_["type"], True, True, self.fromRoot)}'] = localizationKey(self.property_["name"])
        writer.addDefinitionList(defList, 4)
        self.addHtmlBlock('div.result', writer.render())

    def render(self):
        return super().render()

class ConstantBuilder(MarkdownWriter):

    def __init__(self, constant=None, fromRoot=False):
        super().__init__()
        if constant is None:
            constant = {}
        self.constant = constant
        self.fromRoot = fromRoot

    def preRender(self):
        defList = {}
        defList[f'`{self.constant["name"]}`'] = ''
        self.addDefinitionList(defList)
        prefix = 'static ' if self.constant.get('is_static', '') else ''
        prefix += 'read-only ' if self.constant["is_read_only"] else ''
        suffix = f' = {f'"{self.constant["value"]}"' if self.constant["type"]["name"] == 'string' else self.constant["value"]}' if 'value' in self.constant else f': {typeString(self.constant["type"], True)}'
        self.addCodeBlock(f'{prefix}{self.constant["name"]}{suffix};', 'js')
        if 'value' not in self.constant:
            writer = MarkdownWriter()
            defList = {}
            defList[f'`{self.constant["name"]}`：{typeString(self.constant["type"], True, True, self.fromRoot)}'] = localizationKey(self.constant["name"])
            writer.addDefinitionList(defList, 4)
            self.addHtmlBlock('div.result', writer.render())

    def render(self):
        return super().render()

class ClassBuilder(MarkdownWriter):

        def __init__(self, class_=None, fromRoot=False):
            super().__init__()
            if class_ is None:
                class_ = {}
            self.class_ = class_
            self.fromRoot = fromRoot

        def preRender(self):
            version = '1.21.0.20'
            ModuleBuilder.currentClassName = self.class_["name"]
            self.addHeading(f'`{self.class_["name"]}`', 1)
            self.addBlockquote('文档版本：{}'.format(version))
            self.addText(f'`{self.class_["name"]}`类{f'，实现了<code>Iterator&lt;<a href="{generatePath(self.class_["iterator"]["optional_type"])}">{typeString(self.class_["iterator"])}</a>&gt;</code>' if 'iterator' in self.class_ else ''}{f'，扩展自{'、'.join([typeString(base, rich=True, fromRoot=self.fromRoot) for base in self.class_['base_types']])}' if len(self.class_['base_types']) > 0 else ''}。{i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}.{self.class_["name"].lower()}.description') if i18n.contain(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}.{self.class_["name"].lower()}.description') else i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{self.class_["name"].lower()}.description')}')
            if len(self.class_["constants"]) > 0:
                self.addHeading('常量', 2)
                for constant in self.class_["constants"]:
                    builder = ConstantBuilder(constant, self.fromRoot)
                    self.addText(builder.render())
            if len(self.class_["properties"]) > 0:
                self.addHeading('属性', 2)
                for property_ in self.class_["properties"]:
                    builder = PropertyBuilder(property_, self.fromRoot)
                    self.addText(builder.render())
            if 'iterator' in self.class_:
                functions = [
                    {
                        'name': '[Symbol.iterator]',
                        'is_static': False,
                        'is_constructor': False,
                        "privilege": "none",
                        'arguments': [],
                        'return_type': {
                            'name': 'iterator',
                            'iterator_type': self.class_["iterator"]
                        }
                    },
                    {
                        'name': 'next',
                        'is_static': False,
                        'is_constructor': False,
                        "privilege": "none",
                        'arguments': [],
                        'return_type': {
                            'name': 'iterator_result',
                            'iterator_type': self.class_["iterator"]
                        }
                    }
                ]
                self.class_["functions"] = functions + self.class_["functions"]
            if len(self.class_["functions"]) > 0:
                self.addHeading('方法', 2)
                for function in self.class_["functions"]:
                    builder = FunctionBuilder(function, self.fromRoot)
                    self.addText(builder.render())
            ModuleBuilder.currentClassName = ''

        def render(self):
            return super().render()


class InterfaceBuilder(MarkdownWriter):

        def __init__(self, interface=None, fromRoot=False):
            super().__init__()
            if interface is None:
                interface = {}
            self.interface = interface
            self.fromRoot = fromRoot

        def preRender(self):
            version = '1.21.0.20'
            ModuleBuilder.currentClassName = self.interface["name"]
            self.addHeading(f'`{self.interface["name"]}`', 1)
            self.addBlockquote('文档版本：{}'.format(version))
            self.addText(f'`{self.interface["name"]}`接口{f'，扩展自{'、'.join([typeString(base, rich=True, fromRoot=self.fromRoot) for base in self.interface['base_types']])}' if len(self.interface['base_types']) > 0 else ''}。{i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}.{self.interface["name"].lower()}.description') if i18n.contain(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}.{self.interface["name"].lower()}.description') else i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{self.interface["name"].lower()}.description')}')
            if len(self.interface["properties"]) > 0:
                self.addHeading('属性', 2)
                for property_ in self.interface["properties"]:
                    builder = PropertyBuilder(property_, self.fromRoot)
                    self.addText(builder.render())
            ModuleBuilder.currentClassName = ''

        def render(self):
            return super().render()

class EnumBuilder(MarkdownWriter):

        def __init__(self, enum=None, fromRoot=False):
            super().__init__()
            if enum is None:
                enum = {}
            self.enum = enum
            self.fromRoot = fromRoot

        def preRender(self):
            version = '1.21.0.20'
            ModuleBuilder.currentClassName = self.enum["name"]
            self.addHeading(f'`{self.enum["name"]}`', 1)
            self.addBlockquote('文档版本：{}'.format(version))
            self.addText(f'`{self.enum["name"]}`枚举。{i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}.{self.enum["name"].lower()}.description') if i18n.contain(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}.{self.enum["name"].lower()}.description') else i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{self.enum["name"].lower()}.description')}')
            if len(self.enum["constants"]) > 0:
                self.addHeading('常量', 2)
                for constant in self.enum["constants"]:
                    builder = ConstantBuilder(constant, self.fromRoot)
                    self.addText(builder.render())
            ModuleBuilder.currentClassName = ''

        def render(self):
            return super().render()


class TypeAliasBuilder(MarkdownWriter):

        def __init__(self, typeAlias=None, fromRoot=False):
            super().__init__()
            if typeAlias is None:
                typeAlias = {}
            self.typeAlias = typeAlias
            self.fromRoot = fromRoot

        def preRender(self):
            version = '1.21.0.20'
            ModuleBuilder.currentClassName = self.typeAlias["name"]
            self.addHeading(f'`{self.typeAlias["name"]}`', 1)
            self.addBlockquote('文档版本：{}'.format(version))
            self.addText(f'`{self.typeAlias["name"]}`类型别名。{i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}.{self.typeAlias["name"].lower()}.description') if i18n.contain(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}.{self.typeAlias["name"].lower()}.description') else i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{self.typeAlias["name"].lower()}.description')}')
            if self.typeAlias["alias_type"] == 'type_map':
                self.addHeading('类型映射', 2)
                defList = {}
                for map in self.typeAlias["mappings"]:
                    defList[f'`{map["name"]}`：[`{map["value"]}`](./{map["value"].lower()}.md)'] = '映射。'
                self.addDefinitionList(defList)
            ModuleBuilder.currentClassName = ''


        def render(self):
            return super().render()


class ErrorBuilder(MarkdownWriter):

        def __init__(self, error=None, fromRoot=False):
            super().__init__()
            if error is None:
                error = {}
            self.error = error
            self.fromRoot = fromRoot

        def preRender(self):
            version = '1.21.0.20'
            ModuleBuilder.currentClassName = self.error["name"]
            self.addHeading(f'`{self.error["name"]}`', 1)
            self.addBlockquote('文档版本：{}'.format(version))
            self.addText(f'`{self.error["name"]}`错误，扩展自`Error`。{i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}.{self.error["name"].lower()}.description') if i18n.contain(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{ModuleBuilder.currentModuleVersion.lower()}.{self.error["name"].lower()}.description') else i18n.get(f'script_api.{ModuleBuilder.currentModuleName.lower()}.{self.error["name"].lower()}.description')}')
            if len(self.error["properties"]) > 0:
                self.addHeading('属性', 2)
                for property_ in self.error["properties"]:
                    builder = PropertyBuilder(property_, self.fromRoot)
                    self.addText(builder.render())
            ModuleBuilder.currentClassName = ''

        def render(self):
            return super().render()

class ModuleBuilder(MarkdownWriter):
        currentModuleName = ''
        currentModuleVersion = ''
        currentClassName = ''

        def __init__(self, module=None):
            super().__init__()
            if module is None:
                module = {}
            self.module = module

        def preRender(self):
            version = '1.21.0.20'
            ModuleBuilder.currentModuleName = self.module["name"]
            ModuleBuilder.currentModuleVersion = self.module["version"]
            if re.match(r'.*?-beta', ModuleBuilder.currentModuleVersion):
                ModuleBuilder.currentModuleVersion = 'beta'
            if re.match(r'.*?-internal', ModuleBuilder.currentModuleVersion):
                ModuleBuilder.currentModuleVersion = 'internal'
            self.addHeading(f'`{self.module["name"]}`', 1)
            self.addBlockquote('文档版本：{}'.format(version))
            self.addText(f'`{self.module["name"]}`模块的`{self.module["version"]}`版本，UUID为`{self.module["uuid"]}`。该模块是{i18n.get(f'script_api.{self.module["name"].lower()}.description')}')
            if self.module["dependencies"]:
                self.addAdmonition('依赖', '该模块依赖于以下模块：\n\n- {}'.format('\n- '.join([f'`{dependency["name"]}`|`{dependency["version"]}`|`{dependency["uuid"]}`' for dependency in self.module["dependencies"]])), 'info')
            if self.module["constants"]:
                self.addHeading('常量', 2)
                for constant in self.module["constants"]:
                    builder = ConstantBuilder(constant, True)
                    self.addText(builder.render())
            if self.module["objects"]:
                self.addHeading('对象', 2)
                for object in self.module["objects"]:
                    builder = PropertyBuilder(object, True)
                    self.addText(builder.render())
            if self.module["functions"]:
                self.addHeading('函数', 2)
                for function in self.module["functions"]:
                    builder = FunctionBuilder(function, True)
                    self.addText(builder.render())
            if self.module["classes"]:
                self.addHeading('类', 2)
                self.addTable(['类', '描述'], [[f'[`{class_["name"]}`](./{class_["name"].lower()}.md)', ''] for class_ in self.module["classes"]])
            if self.module["interfaces"]:
                self.addHeading('接口', 2)
                self.addTable(['接口', '描述'], [[f'[`{interface["name"]}`](./{interface["name"].lower()}.md)', ''] for interface in self.module["interfaces"]])
            if self.module["enums"]:
                self.addHeading('枚举', 2)
                self.addTable(['枚举', '描述'], [[f'[`{enum["name"]}`](./{enum["name"].lower()}.md)', ''] for enum in self.module["enums"]])
            if self.module["type_aliases"]:
                self.addHeading('类型别名', 2)
                self.addTable(['类型别名', '描述'], [[f'[`{typeAlias["name"]}`](./{typeAlias["name"].lower()}.md)', ''] for typeAlias in self.module["type_aliases"]])
            if self.module["errors"]:
                self.addHeading('错误', 2)
                self.addTable(['错误', '描述'], [[f'[`{error["name"]}`](./{error["name"].lower()}.md)', ''] for error in self.module["errors"]])

        def render(self):
            return super().render()



def argumentSignature(arguments):
    return ', '.join([f'{arg["name"]}{'?' if arg["type"]["name"] == 'optional' else ''}: {typeString(arg["type"])}' for arg in arguments])

def typeString(type, parseOptional=False, rich=False, fromRoot=False):
    prefix = '../'
    if fromRoot:
        prefix = ''
    if type["name"] == 'optional':
        if parseOptional:
            if rich:
                return f'{typeString(type["optional_type"], rich=True, fromRoot=fromRoot)}|`undefined`'
            else:
                return f'{typeString(type["optional_type"])} | undefined'
        else:
            return f'{typeString(type["optional_type"])}'
    elif type["name"] == 'variant':
        if rich:
            return '|'.join([typeString(t, rich=True, fromRoot=fromRoot) for t in type["variant_types"]])
        else:
            return ' | '.join([typeString(t) for t in type["variant_types"]])
    elif type["name"] == 'closure':
        arguments = []
        i = 1
        for arg in type["closure_type"]["argument_types"]:
            arguments.append({'name': 'arg' + (str(i) if i > 1 else ''), 'type': arg})
        if rich:
            signatures = []
            for arg in arguments:
                if arg["type"]["is_bind_type"]:
                    signatures.append(f'<a href="{generatePath(arg["type"], prefix=prefix)}">{typeString(arg["type"])}</a>')
                else:
                    signatures.append(typeString(arg["type"]))
            returnLink = f'<a href="{generatePath(type["closure_type"]["return_type"], prefix=prefix)}">{typeString(type["closure_type"]["return_type"])}</a>' if type["closure_type"]["return_type"]["is_bind_type"] else typeString(type["closure_type"]["return_type"])
            return f'<code>({", ".join(signatures)}) =&gt; {returnLink}</code>'
        return f'({argumentSignature(arguments)}) => {typeString(type["closure_type"]["return_type"])}'
    elif type["name"] == 'array':
        if rich:
            if type["element_type"]["is_bind_type"]:
                return f'<code><a href="{generatePath(type["element_type"], prefix=prefix)}">{typeString(type["element_type"])}</a>[]</code>'
            else:
                return f'`{'(' if type["element_type"]["name"] == 'variant' else ''}{typeString(type["element_type"])}{')' if type["element_type"]["name"] == 'variant' else ''}[]`'
        else:
            return f'{'(' if type["element_type"]["name"] == 'variant' else ''}{typeString(type["element_type"])}{')' if type["element_type"]["name"] == 'variant' else ''}[]'
    elif type["name"] == 'generator':
        if rich:
            if type["generator_type"]["yield_type"]["is_bind_type"] or type["generator_type"]["next_type"]["is_bind_type"] or type["generator_type"]["return_type"]["is_bind_type"]:
                yieldLink = f'<a href="{generatePath(type["generator_type"]["yield_type"], prefix=prefix)}">{typeString(type["generator_type"]["yield_type"])}</a>' if type["generator_type"]["yield_type"]["is_bind_type"] else typeString(type["generator_type"]["yield_type"])
                nextLink = f'<a href="{generatePath(type["generator_type"]["next_type"], prefix=prefix)}">{typeString(type["generator_type"]["next_type"])}</a>' if type["generator_type"]["next_type"]["is_bind_type"] else typeString(type["generator_type"]["next_type"])
                returnLink = f'<a href="{generatePath(type["generator_type"]["return_type"], prefix=prefix)}">{typeString(type["generator_type"]["return_type"])}</a>' if type["generator_type"]["return_type"]["is_bind_type"] else typeString(type["generator_type"]["return_type"])
                return f'<code>Generator&lt;{yieldLink}, {nextLink}, {returnLink}&gt;</code>'
            else:
                return f'`Generator<{typeString(type["generator_type"]["yield_type"])}, {typeString(type["generator_type"]["next_type"])}, {typeString(type["generator_type"]["return_type"])}>`'
        else:
            return f'Generator<{typeString(type["generator_type"]["yield_type"])}, {typeString(type["generator_type"]["next_type"])}, {typeString(type["generator_type"]["return_type"])}>'
    elif type["name"] == 'map':
        if rich:
            if type["key_type"]["is_bind_type"] or type["value_type"]["is_bind_type"]:
                keyLink = f'<a href="{generatePath(type["key_type"], prefix=prefix)}">{typeString(type["key_type"])}</a>' if type["key_type"]["is_bind_type"] else typeString(type["key_type"])
                valueLink = f'<a href="{generatePath(type["value_type"], prefix=prefix)}">{typeString(type["value_type"])}</a>' if type["value_type"]["is_bind_type"] else typeString(type["value_type"])
                return f'<code>Record&lt;{keyLink}, {valueLink}&gt;</code>'
            else:
                return f'`Record<{typeString(type["key_type"])}, {typeString(type["value_type"])}>`'
        else:
            return f'Record<{typeString(type["key_type"])}, {typeString(type["value_type"])}>'
    elif type["name"] == 'promise':
        if rich:
            if type["promise_type"]["is_bind_type"]:
                return f'<code>Promise&lt;<a href="{generatePath(type["promise_type"], prefix=prefix)}">{typeString(type["promise_type"])}</a>&gt;</code>'
            else:
                return f'`Promise<{typeString(type["promise_type"])}>`'
        else:
            return f'Promise<{typeString(type["promise_type"])}>'
    elif type["name"] == 'iterator':
        if rich:
            if type["iterator_type"]["optional_type"]["is_bind_type"]:
                return f'<code>Iterator&lt;<a href="{generatePath(type["iterator_type"]["optional_type"], prefix=prefix)}">{typeString(type["iterator_type"])}</a>&gt;</code>'
            else:
                return f'`Iterator<{typeString(type["iterator_type"])}>`'
        else:
            return f'Iterator<{typeString(type["iterator_type"])}>'
    elif type["name"] == 'iterator_result':
        if rich:
            if type["iterator_type"]["optional_type"]["is_bind_type"]:
                return f'<code>IteratorResult&lt;<a href="{generatePath(type["iterator_type"]["optional_type"], prefix=prefix)}">{typeString(type["iterator_type"])}</a>&gt;</code>'
            else:
                return f'`IteratorResult<{typeString(type["iterator_type"])}>`'
        else:
            return f'IteratorResult<{typeString(type["iterator_type"])}>'
    elif type["name"] == 'undefined':
        if rich:
            return '`void`'
        else:
            return 'void'
    else:
        if rich:
            if type["is_bind_type"]:
                return f'[`{type["name"]}`]({generateMDPath(type)})'
            else:
                return f'`{type["name"]}`'
        else:
            return type["name"]


def parseFromModule(obj):
    name = obj["name"]
    if name == 'mojang-minecraft':
        name = 'server'
    elif name == 'mojang-minecraft-ui':
        name = 'server-ui'
    else:
        name = re.sub(r"@minecraft/(.*)", r"\1", name)
    version = obj["version"]
    if re.findall('beta', version):
        version = 'beta'
    elif re.findall('internal', version):
        version = 'internal'
    return f'{name}/{version}'


def generateMDPath(type, suffix='.md'):
    return generatePath(type, suffix, '')

def generatePath(type, suffix='/', prefix='../'):
    if 'from_module' in type:
        module = parseFromModule(type["from_module"])
        return f'{prefix}../../{module}/{type["name"].lower()}{suffix}'
    else:
        return f'{prefix if prefix else './'}{type["name"].lower()}{suffix}'
