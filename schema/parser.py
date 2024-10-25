import json5, json, os


class SchemaParser:
    def __init__(self):
        self.schema = {}
        self.schemaPath = ''
        self.data = {}
        self.dataPath = ''
        self.references = {}
        self.outputPath = ''

    def readSchema(self, schemaPath):
        self.schemaPath = os.path.abspath(schemaPath)
        with open(schemaPath, 'r', encoding="utf-8") as f:
            self.schema = json5.load(f)

    def readData(self, dataPath):
        self.dataPath = os.path.abspath(dataPath)
        with open(dataPath, 'r', encoding="utf-8") as f:
            self.data = json5.load(f)

    def setOutputPath(self, outputPath):
        self.outputPath = os.path.abspath(outputPath)

    def outputData(self):
        dirName = os.path.dirname(self.outputPath)
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        with open(self.outputPath, 'w', encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def convertSchema2Data(self):
        self.data = self.convertSubschema2Data('top', self.schema)
        if len(self.references) > 0:
            self.data['definition_types'] = self.references
            self.references = []

    def convertSubschema2Data(self, key, subschema):
        data = {}
        data['name'] = key
        data['type'] = self.convertSubschemaType2Data(subschema)
        data['details'] = {}
        details = data['details']
        if 'default' in subschema:
            details['default_value'] = subschema['default']
        if details == {}:
            del data['details']
        return data

    def convertSubschemaType2Data(self, subschema):
        commonSubschema = subschema
        type = {}
        type['name'] = self.determineSubschemaType(subschema)
        if type['name'] == 'reference':
            type['reference'] = subschema['$ref'].replace('#/definitions/', '#/definition_types/')
            if subschema['$ref'].startswith('#/definitions/'):
                refKey = subschema['$ref'].replace('#/definitions/', '')
                if refKey not in self.references:
                    self.references[refKey] = {}
                    self.references[refKey] = self.convertSubschemaType2Data(self.schema['definitions'][refKey])
            else:
                if not os.path.exists(os.path.join(os.path.dirname(self.outputPath), subschema['$ref'])):
                    parser = SchemaParser()
                    parser.readSchema(os.path.join(os.path.dirname(self.schemaPath), subschema['$ref']))
                    parser.setOutputPath(os.path.join(os.path.dirname(self.outputPath), subschema['$ref']))
                    parser.convertSchema2Data()
                    parser.outputData()
        if type['name'] == 'const':
            type['const_type'] = self.convertSubschemaType2Data(subschema['const'])
        if type['name'] == 'variant':
            type['variant_types'] = []
            if 'oneOf' in commonSubschema:
                type['variant_types'] += [self.convertSubschemaType2Data(subschema['oneOf'][i]) for i in range(len(subschema['oneOf']))]
                del commonSubschema['oneOf']
            if 'anyOf' in commonSubschema:
                type['variant_types'] += [self.convertSubschemaType2Data(subschema['anyOf'][i]) for i in range(len(subschema['anyOf']))]
                del commonSubschema['anyOf']
            type['common_type'] = self.convertSubschemaType2Data(commonSubschema)
        if type['name'] == 'intersection':
            type['intersection_types'] = [self.convertSubschemaType2Data(subschema['allOf'][i]) for i in range(len(subschema['allOf']))]
            del commonSubschema['allOf']
            type['common_type'] = self.convertSubschemaType2Data(commonSubschema)
        if type['name'] == 'conditional':
            type['conditional_type'] = self.convertSubschemaType2Data(subschema['if'])
            if 'then' in subschema:
                type['then_type'] = self.convertSubschemaType2Data(subschema['then'])
            if 'else' in subschema:
                type['else_type'] = self.convertSubschemaType2Data(subschema['else'])
            del commonSubschema['if']
            if 'then' in commonSubschema:
                del commonSubschema['then']
            if 'else' in commonSubschema:
                del commonSubschema['else']
            type['common_type'] = self.convertSubschemaType2Data(commonSubschema)
        if type['name'] == 'enum':
            type['enum_values'] = subschema['enum']
        if type['name'] == 'object':
            if 'properties' in subschema:
                type['properties'] = [self.convertSubschema2Data(key, subschema['properties'][key]) for key in subschema['properties']]
            if 'additionalProperties' in subschema:
                type['additional_property_type'] = self.convertSubschemaType2Data(subschema['additionalProperties'])
            if 'patternProperties' in subschema:
                type['pattern_property_types'] = [self.convertSubschema2Data(key, subschema['patternProperties'][key]) for key in subschema['patternProperties']]
        if type['name'] == 'array':
            if 'items' in subschema:
                if isinstance(subschema['items'], list):
                    type['element_types'] = [self.convertSubschemaType2Data(subschema['items'][i]) for i in range(len(subschema['items']))]
                else:
                    type['additional_element_type'] = self.convertSubschemaType2Data(subschema['items'])
            if 'additionalItems' in subschema:
                type['additional_element_type'] = self.convertSubschemaType2Data(subschema['additionalItems'])
            if 'contains' in subschema:
                type['contains_type'] = self.convertSubschemaType2Data(subschema['contains'])
            if 'minItems' in subschema:
                type['min_items'] = subschema['minItems']
            if 'maxItems' in subschema:
                type['max_items'] = subschema['maxItems']
        if type['name'] == 'string':
            if 'minLength' in subschema:
                type['min_length'] = subschema['minLength']
            if 'maxLength' in subschema:
                type['max_length'] = subschema['maxLength']
            if 'pattern' in subschema:
                type['pattern'] = subschema['pattern']
        if type['name'] == 'number' or type['name'] == 'integer':
            if 'minimum' in subschema:
                type['minimum'] = subschema['minimum']
            if 'maximum' in subschema:
                type['maximum'] = subschema['maximum']
            if 'exclusiveMinimum' in subschema:
                type['exclusive_minimum'] = subschema['exclusiveMinimum']
            if 'exclusiveMaximum' in subschema:
                type['exclusive_maximum'] = subschema['exclusiveMaximum']
            if 'multipleOf' in subschema:
                type['multiple_of'] = subschema['multipleOf']
        if type['name'] == 'boolean':
            pass
        if type['name'] == 'null':
            pass
        if type['name'] == 'tautology':
            type['correctness'] = subschema
        elif '$comment' in subschema:
            comments = subschema['$comment'].split(';')
            type.update(self.parseCommnents(comments))
        if type['name'] == 'unknown':
            return {}
        return type

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
        if 'if' in subschema:
            return 'conditional'
        if 'enum' in subschema:
            return 'enum'
        if 'type' in subschema:
            return subschema['type']
        if 'properties' in subschema or 'additionalProperties' in subschema or 'patternProperties' in subschema:
            return 'object'
        if 'items' in subschema or 'additionalItems' in subschema or 'contains' in subschema:
            return 'array'
        return 'unknown'

    def parseCommnents(self, comments):
        type = {}
        for comment in comments:
            if comment == '':
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

