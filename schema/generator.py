

import json5, json
import os
import shutil
from schema.parser import SchemaParser
from schema.convertor import SchemaConvertor


class SchemaDataGenerator(object):
    def __init__(self):
        self.baseFiles = [
            'assets/schemas/behavior/items/item.json',
            'assets/schemas/behavior/blocks/block.json',
            'assets/schemas/behavior/entities/entity.json'
        ]

    def generate(self):
        shutil.rmtree('assets/extra/schema', ignore_errors=True)
        for baseFile in self.baseFiles:
            parser = SchemaParser()
            parser.readSchema(baseFile)
            parser.setOutputPath(baseFile.replace('assets/schemas', 'assets/extra/schema'))
            parser.convertSchema2Data()
            parser.outputData()


class SchemaDataConvertor(object):
    def __init__(self):
        pass

    def generate(self):
        shutil.rmtree('assets/extra/data-driven/docs', ignore_errors=True)
        shutil.rmtree('assets/extra/data-driven/wiki', ignore_errors=True)
        shutil.rmtree('assets/extra/data-driven/blockception', ignore_errors=True)
        for root, dirs, files in os.walk('assets/docs/json_schemas'):
            for file in files:
                if file.endswith('.json'):
                    print(f'Converting {os.path.join(root, file)}')
                    convertor = SchemaConvertor()
                    convertor.readSchema(os.path.join(root, file))
                    convertor.setOutputPath(os.path.join('assets/extra/data-driven/docs', os.path.relpath(root, 'assets/docs/json_schemas'), file))
                    convertor.convert()
                    convertor.outputData()
        for root, dirs, files in os.walk('assets/schemas/merged'):
            for file in files:
                if file.endswith('.json'):
                    print(f'Converting {os.path.join(root, file)}')
                    convertor = SchemaConvertor()
                    convertor.readSchema(os.path.join(root, file))
                    convertor.setOutputPath(os.path.join('assets/extra/data-driven/wiki', os.path.relpath(root, 'assets/schemas/merged'), file))
                    convertor.convert()
                    convertor.outputData()
        for root, dirs, files in os.walk('assets/schemas-blockception/merged'):
            for file in files:
                if file.endswith('.json'):
                    print(f'Converting {os.path.join(root, file)}')
                    convertor = SchemaConvertor()
                    convertor.readSchema(os.path.join(root, file))
                    convertor.setOutputPath(os.path.join('assets/extra/data-driven/blockception', os.path.relpath(root, 'assets/schemas-blockception/merged'), file))
                    convertor.convert()
                    convertor.outputData()