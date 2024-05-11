from markdown.writer import *

import os
import json5, json

class SchemaBuilder(MarkdownWriter):

    def __init__(self, schema, path):
        super().__init__()
        self.entry = schema
        self.basePath = path
        self.components = []
        self.conditions = []
        self.isComponent = False

    def preRender(self):
        version = '1.21.0.24'
        title = self.entry.get('title', '未命名')
        self.addHeading(title, 1)
        self.addBlockquote('文档版本：{}'.format(version))
        self.addText(self.entry.get('description', ''))
        self.addHeading('架构', 2)
        self.addText(buildNode(self, '', self.entry, self.basePath, self.entry.get('definitions', {}), [], 3, True))


    def render(self):
        return super().render()


def getAbsolutePath(path, ref):
    return os.path.abspath(os.path.join(path, ref)).split('bedrock-docs-generator\\')[-1].split('bedrock-docs-generator/')[-1]

def getId(ref, default):
    return ref['$id'].split('.')[-1] if '$id' in ref else (ref['title'].lower().replace(' ', '_') if 'title' in ref else default)

def buildNode(cls, key, _subschema, path, defs, recordedRefs, level=3, newFile=False):
    subschema = {}
    subschema.update(_subschema)
    required = _subschema.get('required', [])
    writer = MarkdownWriter()
    if '$ref' in subschema:
        if not subschema["$ref"].startswith('#'):
            newId = ''
            if getAbsolutePath(path, subschema["$ref"]) not in recordedRefs:
                recordedRefs.append(getAbsolutePath(path, subschema["$ref"]))
                with open(getAbsolutePath(path, subschema["$ref"]), 'r', encoding="utf-8") as f:
                    # print(getAbsolutePath(path, subschema["$ref"]))
                    ref = json5.load(f)
                    # ref = json.load(f)
                    newId = getId(ref, subschema["$ref"].split('/')[-1].replace('.json', '').lower())
                    if newId == 'filters':
                        if not newFile:
                            defList = {}
                            defList[f'`{key}`：<samp>{newId}</samp>'] = f'一个[过滤器组]({'.' if cls.isComponent else ''}./filter.md)。' + subschema.get('description', '')
                            writer.addDefinitionList(defList, level)
                    else:
                        if not newFile:
                            defList = {}
                            defList[f'`{key}`：<samp>{newId}</samp> {{#{getAbsolutePath(path, subschema["$ref"]).replace('/', '.').replace('\\', '.').replace(':', '.')}}}'] = subschema.get('description', '')
                            writer.addDefinitionList(defList, level)
                        writer.addText(buildNode(cls, subschema["$ref"].split('/')[-1].replace('.json', '').lower(), ref, os.path.dirname(getAbsolutePath(path, subschema["$ref"])), ref.get('definitions', {}), recordedRefs, level, True))
            else:
                with open(getAbsolutePath(path, subschema["$ref"]), 'r', encoding="utf-8") as f:
                    # print(getAbsolutePath(path, subschema["$ref"]))
                    ref = json5.load(f)
                    # ref = json.load(f)
                    newId = getId(ref, subschema["$ref"].split('/')[-1].replace('.json', '').lower())
                    if newId == 'filters':
                        if not newFile:
                            defList = {}
                            defList[f'`{key}`：<samp>{newId}</samp>'] = f'一个[过滤器组]({'.' if cls.isComponent else ''}./filter.md)。' + subschema.get('description', '')
                            writer.addDefinitionList(defList, level)
                    else:
                        if not newFile:
                            defList = {}
                            defList[f'`{key}`：<samp>[{newId}](#{getAbsolutePath(path, subschema["$ref"]).replace('/', '.').replace('\\', '.').replace(':', '.')})</samp>'] = subschema.get('description', '')
                            writer.addDefinitionList(defList, level)
            return writer.render()
        else:
            subschema.update(defs[subschema["$ref"].replace('#/definitions/', '')])
            if subschema["$ref"] not in recordedRefs:
                recordedRefs.append(subschema["$ref"])
            else:
                if 'properties' in subschema:
                    subschema.pop('properties')
                if 'additionalProperties' in subschema:
                    subschema.pop('additionalProperties')
                if 'patternProperties' in subschema:
                    subschema.pop('patternProperties')
                if 'items' in subschema:
                    subschema.pop('items')
                if 'additionalItems' in subschema:
                    subschema.pop('additionalItems')
                if 'oneOf' in subschema:
                    subschema.pop('oneOf')
                if 'anyOf' in subschema:
                    subschema.pop('anyOf')
                if 'allOf' in subschema:
                    subschema.pop('allOf')
                if 'then' in subschema:
                    subschema.pop('then')
                if 'else' in subschema:
                    subschema.pop('else')
            subschema.pop('$ref')
    if 'oneOf' in subschema or 'anyOf' in subschema or 'allOf' in subschema or 'then' in subschema or 'else' in subschema:
        if 'oneOf' in subschema:
            for oneOf in subschema['oneOf']:
                _oneOf = {}
                _oneOf.update(subschema)
                _oneOf.pop('oneOf')
                if 'anyOf' in _oneOf:
                    _oneOf.pop('anyOf')
                if 'allOf' in _oneOf:
                    _oneOf.pop('allOf')
                if 'then' in _oneOf:
                    _oneOf.pop('then')
                if 'else' in _oneOf:
                    _oneOf.pop('else')
                _oneOf.update(oneOf)
                writer.addText(buildNode(cls, key, _oneOf, path, defs, recordedRefs, level, newFile))
        if 'anyOf' in subschema:
            for anyOf in subschema['anyOf']:
                _anyOf = {}
                _anyOf.update(subschema)
                if 'oneOf' in _anyOf:
                    _anyOf.pop('oneOf')
                _anyOf.pop('anyOf')
                if 'allOf' in _anyOf:
                    _anyOf.pop('allOf')
                if 'then' in _anyOf:
                    _anyOf.pop('then')
                if 'else' in _anyOf:
                    _anyOf.pop('else')
                _anyOf.update(anyOf)
                writer.addText(buildNode(cls, key, _anyOf, path, defs, recordedRefs, level, newFile))
        if 'allOf' in subschema:
            for allOf in subschema['allOf']:
                _allOf = {}
                _allOf.update(subschema)
                if 'oneOf' in _allOf:
                    _allOf.pop('oneOf')
                if 'anyOf' in _allOf:
                    _allOf.pop('anyOf')
                _allOf.pop('allOf')
                if 'then' in _allOf:
                    _allOf.pop('then')
                if 'else' in _allOf:
                    _allOf.pop('else')
                _allOf.update(allOf)
                writer.addText(buildNode(cls, key, _allOf, path, defs, recordedRefs, level, newFile))
        if 'then' in subschema:
            then = subschema['then']
            _then = {}
            _then.update(subschema)
            if 'oneOf' in _then:
                _then.pop('oneOf')
            if 'anyOf' in _then:
                _then.pop('anyOf')
            if 'allOf' in _then:
                _then.pop('allOf')
            _then.pop('then')
            if 'else' in _then:
                _then.pop('else')
            _then.update(then)
            writer.addText(buildNode(cls, key, _then, path, defs, recordedRefs, level, newFile))
        if 'else' in subschema:
            els = subschema['else']
            _else = {}
            _else.update(subschema)
            if 'oneOf' in _else:
                _else.pop('oneOf')
            if 'anyOf' in _else:
                _else.pop('anyOf')
            if 'allOf' in _else:
                _else.pop('allOf')
            if 'then' in _else:
                _else.pop('then')
            _else.pop('else')
            _else.update(els)
            writer.addText(buildNode(cls, key, _else, path, defs, recordedRefs, level, newFile))
    else:
        if 'enum' in subschema and 'type' not in subschema:
            if isinstance(subschema['enum'][0], str):
                subschema['type'] = 'string'
            elif isinstance(subschema['enum'][0], int):
                subschema['type'] = 'int'
            elif isinstance(subschema['enum'][0], float):
                subschema['type'] = 'number'
            elif isinstance(subschema['enum'][0], bool):
                subschema['type'] = 'boolean'
            elif isinstance(subschema['enum'][0], list):
                subschema['type'] = 'array'
            else:
                subschema['type'] = 'object'
        if ('properties' in subschema or 'patternProperties' in subschema or 'additionalProperties' in subschema) and 'type' not in subschema:
            subschema['type'] = 'object'
        if ('items' in subschema or 'additionalItems' in subschema) and 'type' not in subschema:
            subschema['type'] = 'array'
        if 'type' in subschema:
            propertiesWriter = MarkdownWriter()
            # print(key)
            if subschema['type'] == 'object':
                pattern = ''
                minLength = 0
                maxLength = 0
                if 'propertyNames' in subschema:
                    pattern = subschema['propertyNames'].get('pattern', '')
                    minLength = subschema['propertyNames'].get('minLength', 0)
                    maxLength = subschema['propertyNames'].get('maxLength', 0)
                if 'properties' in subschema:
                    for keyProp in subschema['properties']:
                        if key == 'components' and '$ref' in subschema['properties'][keyProp]:
                            with open(getAbsolutePath(path, subschema['properties'][keyProp]["$ref"]), 'r', encoding="utf-8") as f:
                                ref = json5.load(f)
                                # ref = json.load(f)
                                newId = getId(ref, subschema['properties'][keyProp]["$ref"].split('/')[-1].replace('.json', '').lower())
                                cls.components.append((keyProp, getAbsolutePath(path, subschema['properties'][keyProp]["$ref"])))
                                defList = {}
                                defList[f'`{keyProp}`：<samp>{newId}</samp>'] = f'[`{keyProp}`]({'.' if cls.isComponent else ''}./components/{getAbsolutePath(path, subschema['properties'][keyProp]["$ref"]).split('/')[-1].split('\\')[-1].replace('.json', '')}.md)组件。' + subschema.get('description', '')
                                propertiesWriter.addDefinitionList(defList, level + 1)
                        elif key == 'conditions' and '$ref' in subschema['properties'][keyProp]:
                            with open(getAbsolutePath(path, subschema['properties'][keyProp]["$ref"]), 'r', encoding="utf-8") as f:
                                ref = json5.load(f)
                                # ref = json.load(f)
                                newId = getId(ref, subschema['properties'][keyProp]["$ref"].split('/')[-1].replace('.json', '').lower())
                                cls.conditions.append((keyProp, getAbsolutePath(path, subschema['properties'][keyProp]["$ref"])))
                                defList = {}
                                defList[f'`{keyProp}`：<samp>{newId}</samp>'] = f'[`{keyProp}`]({'.' if cls.isComponent else ''}./conditions/{getAbsolutePath(path, subschema['properties'][keyProp]["$ref"]).split('/')[-1].split('\\')[-1].replace('.json', '')}.md)条件。' + subschema.get('description', '')
                                propertiesWriter.addDefinitionList(defList, level + 1)
                        elif isinstance(subschema['properties'][keyProp], dict):
                            propertiesWriter.addText(buildNode(cls, keyProp, subschema['properties'][keyProp], path, defs, recordedRefs, level + 1, False))
                if 'patternProperties' in subschema:
                    for keyProp in subschema['patternProperties']:
                        if key == 'components' and '$ref' in subschema['patternProperties'][keyProp]:
                            with open(getAbsolutePath(path, subschema['patternProperties'][keyProp]["$ref"]), 'r', encoding="utf-8") as f:
                                ref = json5.load(f)
                                # ref = json.load(f)
                                newId = getId(ref, subschema['patternProperties'][keyProp]["$ref"].split('/')[-1].replace('.json', '').lower())
                                cls.components.append((keyProp, getAbsolutePath(path, subschema['patternProperties'][keyProp]["$ref"])))
                                defList = {}
                                defList[f'`{keyProp}`：<samp>{newId}</samp>'] = f'[`{keyProp}`]({'.' if cls.isComponent else ''}./components/{getAbsolutePath(path, subschema['patternProperties'][keyProp]["$ref"]).split('/')[-1].split('\\')[-1].replace('.json', '')}.md)组件。' + subschema.get('description', '')
                                propertiesWriter.addDefinitionList(defList, level + 1)
                        elif key == 'conditions' and '$ref' in subschema['patternProperties'][keyProp]:
                            with open(getAbsolutePath(path, subschema['patternProperties'][keyProp]["$ref"]), 'r', encoding="utf-8") as f:
                                ref = json5.load(f)
                                # ref = json.load(f)
                                newId = getId(ref, subschema['patternProperties'][keyProp]["$ref"].split('/')[-1].replace('.json', '').lower())
                                cls.conditions.append((keyProp, getAbsolutePath(path, subschema['patternProperties'][keyProp]["$ref"])))
                                defList = {}
                                defList[f'`{keyProp}`：<samp>{newId}</samp>'] = f'[`{keyProp}`]({'.' if cls.isComponent else ''}./conditions/{getAbsolutePath(path, subschema['patternProperties'][keyProp]["$ref"]).split('/')[-1].split('\\')[-1].replace('.json', '')}.md)条件。' + subschema.get('description', '')
                                propertiesWriter.addDefinitionList(defList, level + 1)
                        elif isinstance(subschema['patternProperties'][keyProp], dict):
                            propertiesWriter.addText(buildNode(cls, keyProp, subschema['patternProperties'][keyProp], path, defs, recordedRefs, level + 1, False))
                if 'additionalProperties' in subschema and isinstance(subschema['additionalProperties'], dict):
                    if key == 'components' and '$ref' in subschema['additionalProperties']:
                        with open(getAbsolutePath(path, subschema['additionalProperties']["$ref"]), 'r', encoding="utf-8") as f:
                            ref = json5.load(f)
                            # ref = json.load(f)
                            newId = getId(ref, subschema['additionalProperties']["$ref"].split('/')[-1].replace('.json', '').lower())
                            cls.components.append(('additionalProperties', getAbsolutePath(path, subschema['additionalProperties']["$ref"])))
                            defList = {}
                            defList[f'`<any object property>`：<samp>{newId}</samp>'] = f'[额外组件]({'.' if cls.isComponent else ''}./components/{getAbsolutePath(path, subschema['additionalProperties']["$ref"]).split('/')[-1].split('\\')[-1].replace('.json', '')}.md)。' + subschema.get('description', '')
                            propertiesWriter.addDefinitionList(defList, level + 1)
                    elif key == 'conditions' and '$ref' in subschema['additionalProperties']:
                        with open(getAbsolutePath(path, subschema['additionalProperties']["$ref"]), 'r', encoding="utf-8") as f:
                            ref = json5.load(f)
                            # ref = json.load(f)
                            newId = getId(ref, subschema['additionalProperties']["$ref"].split('/')[-1].replace('.json', '').lower())
                            cls.conditions.append(('additionalProperties', getAbsolutePath(path, subschema['additionalProperties']["$ref"])))
                            defList = {}
                            defList[f'`<any object property>`：<samp>{newId}</samp>'] = f'[额外条件]({'.' if cls.isComponent else ''}./conditions/{getAbsolutePath(path, subschema['additionalProperties']["$ref"]).split('/')[-1].split('\\')[-1].replace('.json', '')}.md)。' + subschema.get('description', '')
                            propertiesWriter.addDefinitionList(defList, level + 1)
                    else:
                        propertiesWriter.addText(buildNode(cls, pattern if pattern else '<any object property>', subschema['additionalProperties'], path, defs, recordedRefs, level + 1, False))
            elif subschema['type'] == 'array':
                if 'items' in subschema:
                    if isinstance(subschema['items'], dict):
                        propertiesWriter.addText(buildNode(cls, '<any array element>', subschema['items'], path, defs, recordedRefs, level + 1, False))
                    elif isinstance(subschema['items'], list):
                        index = 0
                        for item in subschema['items']:
                            propertiesWriter.addText(buildNode(cls, f'{index}..{index}', item, path, defs, recordedRefs, level + 1, False))
                            index += 1
                elif 'additionalItems' in subschema:
                    propertiesWriter.addText(buildNode(cls, '<any array element>', subschema['additionalItems'], path, defs, recordedRefs, level + 1, False))
            if not newFile:
                defList = {}
                defList[f'`{key}`：<samp>{subschema['type']}</samp>'] = subschema.get('description', '')
                writer.addDefinitionList(defList, level)
                if subschema['type'] == 'object' or subschema['type'] == 'array':
                    writer.addText(f'<div class="language-text highlight"><span class="filename"><code>{key.replace('<', '&lt;').replace('>', '&gt;')}</code></span><pre id="__code_1"><span></span></pre></div>')
                    writer.addHtmlBlock('div.result', propertiesWriter.render(), level)
            else:
                mcschema = buildMcSchema(key, _subschema, path, _subschema.get('definitions', {}), [])
                writer.addCodeBlock(mcschema, 'mcschema')
                writer.addHtmlBlock('div.result', propertiesWriter.render(), level)
        else:
            defList = {}
            defList[f'`{key}`'] = subschema.get('description', '')
            writer.addDefinitionList(defList, level)
    return writer.render()

def buildMcSchema(key, _subschema, path, defs, recordedRefs, level=0):
    subschema = {}
    subschema.update(_subschema)
    required = _subschema.get('required', [])
    content = ''
    if '$ref' in subschema:
        if not subschema["$ref"].startswith('#'):
            newId = ''
            with open(getAbsolutePath(path, subschema["$ref"]), 'r', encoding="utf-8") as f:
                # print(getAbsolutePath(path, subschema["$ref"]))
                ref = json5.load(f)
                # ref = json.load(f)
                newId = ref['$id'].split('.')[-1] if '$id' in ref else (ref['title'].lower().replace(' ', '_') if 'title' in ref else key)
            content += f'{level * '  '}{newId} "{key}"{' : opt' if key in required else ''}\n'
            return content
        else:
            subschema.update(defs[subschema["$ref"].replace('#/definitions/', '')])
            if subschema["$ref"] not in recordedRefs:
                recordedRefs.append(subschema["$ref"])
            else:
                if 'properties' in subschema:
                    subschema.pop('properties')
                if 'additionalProperties' in subschema:
                    subschema.pop('additionalProperties')
                if 'patternProperties' in subschema:
                    subschema.pop('patternProperties')
                if 'items' in subschema:
                    subschema.pop('items')
                if 'additionalItems' in subschema:
                    subschema.pop('additionalItems')
                if 'oneOf' in subschema:
                    subschema.pop('oneOf')
                if 'anyOf' in subschema:
                    subschema.pop('anyOf')
                if 'allOf' in subschema:
                    subschema.pop('allOf')
                if 'then' in subschema:
                    subschema.pop('then')
                if 'else' in subschema:
                    subschema.pop('else')
            subschema.pop('$ref')
    if 'oneOf' in subschema or 'anyOf' in subschema or 'allOf' in subschema or 'then' in subschema or 'else' in subschema:
        if 'oneOf' in subschema:
            for oneOf in subschema['oneOf']:
                _oneOf = {}
                _oneOf.update(subschema)
                _oneOf.pop('oneOf')
                if 'anyOf' in _oneOf:
                    _oneOf.pop('anyOf')
                if 'allOf' in _oneOf:
                    _oneOf.pop('allOf')
                if 'then' in _oneOf:
                    _oneOf.pop('then')
                if 'else' in _oneOf:
                    _oneOf.pop('else')
                _oneOf.update(oneOf)
                content += f'{buildMcSchema(key, _oneOf, path, defs, recordedRefs, level)}'
        if 'anyOf' in subschema:
            for anyOf in subschema['anyOf']:
                _anyOf = {}
                _anyOf.update(subschema)
                if 'oneOf' in _anyOf:
                    _anyOf.pop('oneOf')
                _anyOf.pop('anyOf')
                if 'allOf' in _anyOf:
                    _anyOf.pop('allOf')
                if 'then' in _anyOf:
                    _anyOf.pop('then')
                if 'else' in _anyOf:
                    _anyOf.pop('else')
                _anyOf.update(anyOf)
                content += f'{buildMcSchema(key, _anyOf, path, defs, recordedRefs, level)}'
        if 'allOf' in subschema:
            for allOf in subschema['allOf']:
                _allOf = {}
                _allOf.update(subschema)
                if 'oneOf' in _allOf:
                    _allOf.pop('oneOf')
                if 'anyOf' in _allOf:
                    _allOf.pop('anyOf')
                _allOf.pop('allOf')
                if 'then' in _allOf:
                    _allOf.pop('then')
                if 'else' in _allOf:
                    _allOf.pop('else')
                _allOf.update(allOf)
                content += f'{buildMcSchema(key, _allOf, path, defs, recordedRefs, level)}'
        if 'then' in subschema:
            then = subschema['then']
            _then = {}
            _then.update(subschema)
            if 'oneOf' in _then:
                _then.pop('oneOf')
            if 'anyOf' in _then:
                _then.pop('anyOf')
            if 'allOf' in _then:
                _then.pop('allOf')
            _then.pop('then')
            if 'else' in _then:
                _then.pop('else')
            _then.update(then)
            content += f'{buildMcSchema(key, _then, path, defs, recordedRefs, level)}'
        if 'else' in subschema:
            els = subschema['else']
            _else = {}
            _else.update(subschema)
            if 'oneOf' in _else:
                _else.pop('oneOf')
            if 'anyOf' in _else:
                _else.pop('anyOf')
            if 'allOf' in _else:
                _else.pop('allOf')
            if 'then' in _else:
                _else.pop('then')
            _else.pop('else')
            _else.update(els)
            content += f'{buildMcSchema(key, _else, path, defs, recordedRefs, level)}'
    else:
        if 'enum' in subschema and 'type' not in subschema:
            if isinstance(subschema['enum'][0], str):
                subschema['type'] = 'string'
            elif isinstance(subschema['enum'][0], int):
                subschema['type'] = 'int'
            elif isinstance(subschema['enum'][0], float):
                subschema['type'] = 'number'
            elif isinstance(subschema['enum'][0], bool):
                subschema['type'] = 'boolean'
            elif isinstance(subschema['enum'][0], list):
                subschema['type'] = 'array'
            else:
                subschema['type'] = 'object'
        if ('properties' in subschema or 'patternProperties' in subschema or 'additionalProperties' in subschema) and 'type' not in subschema:
            subschema['type'] = 'object'
        if ('items' in subschema or 'additionalItems' in subschema) and 'type' not in subschema:
            subschema['type'] = 'array'
        if 'type' in subschema:
            if level:
                content += f'{level * '  '}{subschema['type']} "{key}"{' : opt' if key not in required else ''}\n'
            else:
                if subschema['type'] != 'object':
                    content += f'{level * '  '}{subschema['type']}\n'
            if subschema['type'] == 'object':
                content += f'{level * '  '}{{\n'
                # print(key)
                pattern = ''
                minLength = 0
                maxLength = 0
                if 'propertyNames' in subschema:
                    pattern = subschema['propertyNames'].get('pattern', '')
                    minLength = subschema['propertyNames'].get('minLength', 0)
                    maxLength = subschema['propertyNames'].get('maxLength', 0)
                if 'properties' in subschema:
                    for key in subschema['properties']:
                        if isinstance(subschema['properties'][key], dict):
                            content += buildMcSchema(key, subschema['properties'][key], path, defs, recordedRefs, level + 1)
                if 'patternProperties' in subschema:
                    for key in subschema['patternProperties']:
                        if isinstance(subschema['patternProperties'][key], dict):
                            content += buildMcSchema(key, subschema['patternProperties'][key], path, defs, recordedRefs, level + 1)
                if 'additionalProperties' in subschema and isinstance(subschema['additionalProperties'], dict):
                    content += buildMcSchema(pattern if pattern else '<any object property>', subschema['additionalProperties'], path, defs, recordedRefs, level + 1)
                content += f'{level * '  '}}}\n'
            elif subschema['type'] == 'array':
                if 'items' in subschema:
                    if isinstance(subschema['items'], dict):
                        content += f'{level * '  '}{{\n'
                        content += buildMcSchema('<any array element>', subschema['items'], path, defs, recordedRefs, level + 1)
                        content += f'{level * '  '}}}\n'
                    elif isinstance(subschema['items'], list):
                        index = 0
                        content += f'{level * '  '}{{\n'
                        for item in subschema['items']:
                            content += buildMcSchema(f'{index}..{index}', item, path, defs, recordedRefs, level + 1)
                            index += 1
                        content += f'{level * '  '}}}\n'
                elif 'additionalItems' in subschema:
                    content += f'{level * '  '}{{\n'
                    content += buildMcSchema('<any array element>', subschema['additionalItems'], path, defs, recordedRefs, level + 1)
                    content += f'{level * '  '}}}\n'
        else:
            content += f'{level * '  '} "{key}"{' : opt' if key not in required else ''}\n'
    text = (f'{getId(_subschema, key)}:\n' if level == 0 else '') + f'{content}'
    return text