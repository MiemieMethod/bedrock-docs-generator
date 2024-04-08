import re

from markdown.writer import *



class FunctionBuilder(MarkdownWriter):

    def __init__(self, function=None):
        super().__init__()
        if function is None:
            function = {}
        self.function = function

    def preRender(self):
        defList = {}
        defList[f'`{self.function["name"]}`'] = ''
        self.addDefinitionList(defList)
        prefix = 'new ' if self.function["is_constructor"] else ('static ' if self.function["is_static"] else '')
        arguments = argumentSignature(self.function["arguments"])
        self.addCodeBlock(f'{prefix}{self.function["name"]}({arguments}): {typeString(self.function["return_type"], True)}', 'js')
        writer = MarkdownWriter()
        if len(self.function["arguments"]) > 0:
            i = 1
            for argument in self.function["arguments"]:
                defList = {}
                description = f'参数{i}。'
                i += 1
                defList[f'`{argument["name"]}`：{typeString(argument["type"], True, True)}'] = description
                writer.addDefinitionList(defList, 4)
        writer.addDefinitionList({f'返回值：{typeString(self.function["return_type"], True, True)}': '返回值。'}, 4)
        self.addHtmlBlock('div.result', writer.render())

    def render(self):
        return super().render()



class PropertyBuilder(MarkdownWriter):

    def __init__(self, property_=None):
        super().__init__()
        if property_ is None:
            property_ = {}
        self.property_ = property_

    def preRender(self):
        defList = {}
        defList[f'`{self.property_["name"]}`'] = ''
        self.addDefinitionList(defList)
        prefix = 'static ' if self.property_.get('is_static', '') else ''
        prefix += 'read-only ' if self.property_["is_read_only"] else ''
        self.addCodeBlock(f'{prefix}{self.property_["name"]}: {typeString(self.property_["type"], True)};', 'js')
        writer = MarkdownWriter()
        defList = {}
        defList[f'`{self.property_["name"]}`：{typeString(self.property_["type"], True, True)}'] = '属性。'
        writer.addDefinitionList(defList, 4)
        self.addHtmlBlock('div.result', writer.render())

    def render(self):
        return super().render()

class ConstantBuilder(MarkdownWriter):

    def __init__(self, constant=None):
        super().__init__()
        if constant is None:
            constant = {}
        self.constant = constant

    def preRender(self):
        defList = {}
        defList[f'`{self.constant["name"]}`'] = ''
        self.addDefinitionList(defList)
        prefix = 'static ' if self.constant.get('is_static', '') else ''
        prefix += 'read-only ' if self.constant["is_read_only"] else ''
        self.addCodeBlock(f'{prefix}{self.constant["name"]} = {f'"{self.constant["value"]}"' if self.constant["type"]["name"] == 'string' else self.constant["value"]};', 'js')

    def render(self):
        return super().render()

class ClassBuilder(MarkdownWriter):

        def __init__(self, class_=None):
            super().__init__()
            if class_ is None:
                class_ = {}
            self.class_ = class_

        def preRender(self):
            version = '1.21.0.20'
            self.addHeading(f'`{self.class_["name"]}`', 1)
            self.addBlockquote('文档版本：{}'.format(version))
            self.addText(f'`{self.class_["name"]}`类{f'，实现了<code>Iterator&lt;<a href="{generatePath(self.class_["iterator"])}">{typeString(self.class_["iterator"])}</a>&gt;</code>' if 'iterator' in self.class_ else ''}{f'，扩展自{'、'.join([typeString(base, rich=True) for base in self.class_['base_types']])}' if len(self.class_['base_types']) > 0 else ''}。')
            if len(self.class_["constants"]) > 0:
                self.addHeading('常量', 2)
                for constant in self.class_["constants"]:
                    builder = ConstantBuilder(constant)
                    self.addText(builder.render())
            if len(self.class_["properties"]) > 0:
                self.addHeading('属性', 2)
                for property_ in self.class_["properties"]:
                    builder = PropertyBuilder(property_)
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
                    builder = FunctionBuilder(function)
                    self.addText(builder.render())

        def render(self):
            return super().render()


class InterfaceBuilder(MarkdownWriter):

        def __init__(self, interface=None):
            super().__init__()
            if interface is None:
                interface = {}
            self.interface = interface

        def preRender(self):
            version = '1.21.0.20'
            self.addHeading(f'`{self.interface["name"]}`', 1)
            self.addBlockquote('文档版本：{}'.format(version))
            self.addText(f'`{self.interface["name"]}`接口{f'，扩展自{'、'.join([typeString(base, rich=True) for base in self.interface['base_types']])}' if len(self.interface['base_types']) > 0 else ''}。')
            if len(self.interface["properties"]) > 0:
                self.addHeading('属性', 2)
                for property_ in self.interface["properties"]:
                    builder = PropertyBuilder(property_)
                    self.addText(builder.render())

        def render(self):
            return super().render()

class EnumBuilder(MarkdownWriter):

        def __init__(self, enum=None):
            super().__init__()
            if enum is None:
                enum = {}
            self.enum = enum

        def preRender(self):
            version = '1.21.0.20'
            self.addHeading(f'`{self.enum["name"]}`', 1)
            self.addBlockquote('文档版本：{}'.format(version))
            self.addText(f'`{self.enum["name"]}`枚举。')
            if len(self.enum["constants"]) > 0:
                self.addHeading('常量', 2)
                for constant in self.enum["constants"]:
                    builder = ConstantBuilder(constant)
                    self.addText(builder.render())

        def render(self):
            return super().render()


def argumentSignature(arguments):
    return ', '.join([f'{arg["name"]}{'?' if arg["type"]["name"] == 'optional' else ''}: {typeString(arg["type"])}' for arg in arguments])

def typeString(type, parseOptional=False, rich=False):
    if type["name"] == 'optional':
        if parseOptional:
            if rich:
                return f'{typeString(type["optional_type"], rich=True)}|`undefined`'
            else:
                return f'{typeString(type["optional_type"])} | undefined'
        else:
            return f'{typeString(type["optional_type"])}'
    elif type["name"] == 'variant':
        if rich:
            return '|'.join([typeString(t, rich=True) for t in type["variant_types"]])
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
                    signatures.append(f'<a href="{generatePath(arg["type"])}">{typeString(arg["type"])}</a>')
                else:
                    signatures.append(typeString(arg["type"]))
            returnLink = f'<a href="{generatePath(type["closure_type"]["return_type"])}">{typeString(type["closure_type"]["return_type"])}</a>' if type["closure_type"]["return_type"]["is_bind_type"] else typeString(type["closure_type"]["return_type"])
            return f'<code>({", ".join(signatures)}) =&gt; {returnLink}</code>'
        return f'({argumentSignature(arguments)}) => {typeString(type["closure_type"]["return_type"])}'
    elif type["name"] == 'array':
        if rich:
            if type["element_type"]["is_bind_type"]:
                return f'<code><a href="{generatePath(type["element_type"])}">{typeString(type["element_type"])}</a>[]</code>'
            else:
                return f'`{typeString(type["element_type"])}[]`'
        else:
            return f'{typeString(type["element_type"])}[]'
    elif type["name"] == 'generator':
        if rich:
            if type["generator_type"]["yield_type"]["is_bind_type"] or type["generator_type"]["next_type"]["is_bind_type"] or type["generator_type"]["return_type"]["is_bind_type"]:
                yieldLink = f'<a href="{generatePath(type["generator_type"]["yield_type"])}">{typeString(type["generator_type"]["yield_type"])}</a>' if type["generator_type"]["yield_type"]["is_bind_type"] else typeString(type["generator_type"]["yield_type"])
                nextLink = f'<a href="{generatePath(type["generator_type"]["next_type"])}">{typeString(type["generator_type"]["next_type"])}</a>' if type["generator_type"]["next_type"]["is_bind_type"] else typeString(type["generator_type"]["next_type"])
                returnLink = f'<a href="{generatePath(type["generator_type"]["return_type"])}">{typeString(type["generator_type"]["return_type"])}</a>' if type["generator_type"]["return_type"]["is_bind_type"] else typeString(type["generator_type"]["return_type"])
                return f'<code>Generator&lt;{yieldLink}, {nextLink}, {returnLink}&gt;</code>'
            else:
                return f'`Generator<{typeString(type["generator_type"]["yield_type"])}, {typeString(type["generator_type"]["next_type"])}, {typeString(type["generator_type"]["return_type"])}>`'
        else:
            return f'Generator<{typeString(type["generator_type"]["yield_type"])}, {typeString(type["generator_type"]["next_type"])}, {typeString(type["generator_type"]["return_type"])}>'
    elif type["name"] == 'map':
        if rich:
            if type["key_type"]["is_bind_type"] or type["value_type"]["is_bind_type"]:
                keyLink = f'<a href="{generatePath(type["key_type"])}">{typeString(type["key_type"])}</a>' if type["key_type"]["is_bind_type"] else typeString(type["key_type"])
                valueLink = f'<a href="{generatePath(type["value_type"])}">{typeString(type["value_type"])}</a>' if type["value_type"]["is_bind_type"] else typeString(type["value_type"])
                return f'<code>Record&lt;{keyLink}, {valueLink}&gt;</code>'
            else:
                return f'`Record<{typeString(type["key_type"])}, {typeString(type["value_type"])}>`'
        else:
            return f'Record<{typeString(type["key_type"])}, {typeString(type["value_type"])}>'
    elif type["name"] == 'promise':
        if rich:
            if type["promise_type"]["is_bind_type"]:
                return f'<code>Promise&lt;<a href="{generatePath(type["promise_type"])}">{typeString(type["promise_type"])}</a>&gt;</code>'
            else:
                return f'`Promise<{typeString(type["promise_type"])}>`'
        else:
            return f'Promise<{typeString(type["promise_type"])}>'
    elif type["name"] == 'iterator':
        if rich:
            if type["iterator_type"]["is_bind_type"]:
                return f'<code>Iterator&lt;<a href="{generatePath(type["iterator_type"])}">{typeString(type["iterator_type"])}</a>&gt;</code>'
            else:
                return f'`Iterator<{typeString(type["iterator_type"])}>`'
        else:
            return f'Iterator<{typeString(type["iterator_type"])}>'
    elif type["name"] == 'iterator_result':
        if rich:
            if type["iterator_type"]["is_bind_type"]:
                return f'<code>IteratorResult&lt;<a href="{generatePath(type["iterator_type"])}">{typeString(type["iterator_type"])}</a>&gt;</code>'
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


def generateMDPath(type, prefix='.md'):
    if 'from_module' in type:
        module = parseFromModule(type["from_module"])
        return f'../../{module}/{type["name"].lower()}{prefix}'
    else:
        return f'./{type["name"].lower()}{prefix}'

def generatePath(type, prefix='/'):
    if 'from_module' in type:
        module = parseFromModule(type["from_module"])
        return f'../../../{module}/{type["name"].lower()}{prefix}'
    else:
        return f'../{type["name"].lower()}{prefix}'