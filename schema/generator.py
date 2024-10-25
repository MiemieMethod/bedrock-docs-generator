

import json5, json
import os
import shutil
from schema.parser import SchemaParser


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