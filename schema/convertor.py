import json5, json, os


class SchemaConvertor:
    def __init__(self):
        self.schema = {}
        self.schemaPath = ''
        self.output = {}
        self.outputPath = ''
        self.recordedDefinitions = []
        self.recursiveFiles = [
            r'entities.json',
        ]

    def readSchema(self, schemaPath):
        self.schemaPath = os.path.abspath(schemaPath)
        with open(schemaPath, 'r', encoding="utf-8") as f:
            self.schema = json5.load(f)

    def setOutputPath(self, outputPath):
        self.outputPath = os.path.abspath(outputPath)

    def outputData(self):
        dirName = os.path.dirname(self.outputPath)
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        with open(self.outputPath, 'w', encoding="utf-8") as f:
            json.dump(self.output, f, indent=2)

    def convert(self):
        return self.convertObjectSubschema(self.schema, self.output)

    def convertObjectSubschema(self, subschema, output):
        output["children"] = []
        properties = subschema.get("properties", {})
        for key, value in properties.items():
            children = self.prepareChildren(value, key)
            output["children"] = [*output["children"], *children]
        required = subschema.get("required", [])
        if 'additionalProperties' in subschema:
            if not isinstance(subschema['additionalProperties'], bool):
                children = self.prepareChildren(subschema['additionalProperties'], '<any object property>')
                output["children"] = [*output["children"], *children]
        if 'patternProperties' in subschema:
            for key, value in subschema['patternProperties'].items():
                children = self.prepareChildren(value, key)
                output["children"] = [*output["children"], *children]
        for child in output["children"]:
            if child[1] in required:
                child[2]['required'] = True
            else:
                child[2]['required'] = False

    def convertArraySubschema(self, subschema, output):
        output["children"] = []
        if 'items' in subschema:
            if isinstance(subschema['items'], list):
                for index, item in enumerate(subschema['items']):
                    children = self.prepareChildren(item, f'{index}..{index}')
                    output["children"] = [*output["children"], *children]
            elif isinstance(subschema['items'], dict):
                children = self.prepareChildren(subschema['items'], '<any array element>')
                output["children"] = [*output["children"], *children]
        if 'additionalItems' in subschema:
            if not isinstance(subschema['additionalItems'], bool):
                children = self.prepareChildren(subschema['additionalItems'], '<any array element>')
                output["children"] = [*output["children"], *children]
        if 'contains' in subschema:
            pass

    def prepareChildren(self, subschema, key):
        children = []
        type = self.parseNodeType(subschema)
        if type == 'unknown':
            return children
        if type == 'variant':
            if len(subschema.get('oneOf', [])) > 0:
                for oneOf in subschema['oneOf']:
                    children = [*children, *self.prepareChildren(oneOf, key)]
            if len(subschema.get('anyOf', [])) > 0:
                for anyOf in subschema['anyOf']:
                    children = [*children, *self.prepareChildren(anyOf, key)]
        elif type == 'intersection':
            if len(subschema.get('allOf', [])) > 0:
                for allOf in subschema['allOf']:
                    children = [*children, *self.prepareChildren(allOf, key)]
        elif type == 'conditional':
            if 'if' in subschema:
                children = [*children, *self.prepareChildren(subschema['if'], key)]
            if 'then' in subschema:
                children = [*children, *self.prepareChildren(subschema['then'], key)]
            if 'else' in subschema:
                children = [*children, *self.prepareChildren(subschema['else'], key)]
        else:
            child = []
            child.append(type)
            child.append(key)
            if type == 'object':
                objectSubschema = {}

                if key == 'components':
                    properties = {}
                    originalPropertiesKeys = subschema['properties'].keys()
                    for key in sorted(originalPropertiesKeys):
                        properties[key] = subschema['properties'][key]
                    subschema['properties'] = properties

                self.convertObjectSubschema(subschema, objectSubschema)
                child.append(objectSubschema)
            elif type == 'array':
                arraySubschema = {}
                self.convertArraySubschema(subschema, arraySubschema)
                child.append(arraySubschema)
            else:
                child.append({})

            if isinstance(subschema, dict):
                if 'enum' in subschema:
                    child[2]['enum'] = subschema['enum']
                if 'const' in subschema:
                    child[2]['const'] = subschema['const']
                if 'minLength' in subschema:
                    child[2]['minLength'] = subschema['minLength']
                if 'maxLength' in subschema:
                    child[2]['maxLength'] = subschema['maxLength']
                if 'minimum' in subschema:
                    child[2]['minimum'] = subschema['minimum']
                if 'maximum' in subschema:
                    child[2]['maximum'] = subschema['maximum']
                if 'exclusiveMinimum' in subschema:
                    child[2]['exclusiveMinimum'] = subschema['exclusiveMinimum']
                if 'exclusiveMaximum' in subschema:
                    child[2]['exclusiveMaximum'] = subschema['exclusiveMaximum']
                if 'multipleOf' in subschema:
                    child[2]['multipleOf'] = subschema['multipleOf']
                if 'pattern' in subschema:
                    child[2]['pattern'] = subschema['pattern']
                if 'format' in subschema:
                    child[2]['format'] = subschema['format']
                if 'default' in subschema:
                    child[2]['default'] = subschema['default']
                if 'minProperties' in subschema:
                    child[2]['minProperties'] = subschema['minProperties']
                if 'maxProperties' in subschema:
                    child[2]['maxProperties'] = subschema['maxProperties']
                if 'uniqueItems' in subschema:
                    child[2]['uniqueItems'] = subschema['uniqueItems']
                if 'minItems' in subschema:
                    child[2]['minItems'] = subschema['minItems']
                if 'maxItems' in subschema:
                    child[2]['maxItems'] = subschema['maxItems']
                if '$comment' in subschema:
                    comments = subschema['$comment'].split(';')
                    child[2].update(self.parseCommnents(comments))

            children.append(child)
        return children

    def determineSubschemaType(self, subschema):
        if isinstance(subschema, bool):
            return 'tautology'
        if '$ref' in subschema:
            return 'reference'
        if 'const' in subschema:
            return 'const'
        if 'oneOf' in subschema or 'anyOf' in subschema:
            return 'variant'
        if 'allOf' in subschema:
            return 'intersection'
        if 'enum' in subschema:
            return 'enum'
        if 'type' in subschema:
            return subschema['type']
        if 'properties' in subschema or 'additionalProperties' in subschema or 'patternProperties' in subschema:
            return 'object'
        if 'items' in subschema or 'additionalItems' in subschema or 'contains' in subschema:
            return 'array'
        if 'if' in subschema:
            return 'conditional'
        return 'unknown'

    def parseNodeType(self, subschema):
        type = self.determineSubschemaType(subschema)
        if type == 'object':
            return 'object'
        if type == 'array':
            return 'array'
        if type == 'number':
            return 'float'
        if type == 'integer':
            return 'int'
        if type == 'boolean':
            return 'boolean'
        if type == 'string':
            return 'string'
        if type == 'enum':
            if len(subschema['enum']) == 0:
                return 'null'
            else:
                if isinstance(subschema['enum'][0], str):
                    return 'enum'
                elif isinstance(subschema['enum'][0], int):
                    return 'int'
                elif isinstance(subschema['enum'][0], float):
                    return 'float'
                else:
                    return 'unknown'
        if type == 'reference':
            if (subschema['$ref'] in self.recordedDefinitions and subschema['$ref'].endswith('event')) \
                    or (subschema['$ref'] in self.recordedDefinitions and subschema['$ref'].endswith('1088251937')) \
                    or (subschema['$ref'] in self.recordedDefinitions and subschema['$ref'].endswith('rawtext')) \
                    or (subschema['$ref'] in self.recordedDefinitions and subschema['$ref'].endswith('pools_spec')) \
                    or (subschema['$ref'] in self.recordedDefinitions and subschema['$ref'].endswith('groups_spec')) \
                    or (subschema['$ref'] in self.recordedDefinitions and subschema['$ref'].endswith('grouped-ui')) \
                    or (subschema['$ref'] in self.recordedDefinitions and os.path.basename(self.schemaPath) in self.recursiveFiles):
                return 'recursive'
            if subschema['$ref'].startswith('#/'):
                refSubschemaPath = subschema['$ref'][2:].split('/')
                refSubschema = self.schema
                for path in refSubschemaPath:
                    refSubschema = refSubschema[path]
                self.recordedDefinitions.append(subschema['$ref'])
                subschema.update(refSubschema)
                return self.parseNodeType(refSubschema)
        if type == 'const':
            if isinstance(subschema['const'], str):
                return 'string'
            elif isinstance(subschema['const'], int):
                return 'int'
            elif isinstance(subschema['const'], float):
                return 'float'
            else:
                return 'unknown'
        if type == 'variant':
            return 'variant'
        if type == 'intersection':
            return 'intersection'
        if type == 'conditional':
            return 'conditional'
        if type == 'tautology':
            return 'null'
        return 'unknown'

    def parseCommnents(self, comments):
        type = {}
        for comment in comments:
            if comment == '':
                continue
            if ':' not in comment:
                continue
            key, value = comment.split(':')
            if key == 'version' or key == 'deprecated' or key == 'experiment':
                type[key] = []
                values = value.split('|')
                for val in values:
                    v = {}
                    leftExclusive = False
                    rightExclusive = False
                    if val.startswith('('):
                        leftExclusive = True
                    if val.endswith(')'):
                        rightExclusive = True
                    mm = val.split(',')
                    if len(mm) == 2:
                        v['min'] = mm[0][1:]
                        v['max'] = mm[1][:-1]
                        v['min_exclusivity'] = leftExclusive
                        v['max_exclusivity'] = rightExclusive
                    else:
                        v['value'] = mm[0]
                    type[key].append(v)
            else:
                type[key] = value
        return type