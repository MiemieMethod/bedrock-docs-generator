import json
import os


from table.builder.blockTag import BlockTagBuilder
from table.builder.itemTag import ItemTagBuilder


class TableGenerator(object):
    def __init__(self):
        self.blockTags = {}
        with open(r'assets/data/allay/block_tags.json', 'r') as f:
            self.blockTags = json.load(f)
        self.itemTags = {}
        with open(r'assets/data/allay/item_tags.json', 'r') as f:
            self.itemTags = json.load(f)


    def generate(self):
        if not os.path.exists(r'build'):
            os.mkdir(r'build')
        if not os.path.exists(r'build/tables'):
            os.mkdir(r'build/tables')
        if not os.path.exists(r'build/tables/blocks'):
            os.mkdir(r'build/tables/blocks')
        with open(r'build/tables/blocks/vanilla_tags.md', 'w', encoding="utf-8") as f:
            f.write(BlockTagBuilder(self.blockTags).render())
        if not os.path.exists(r'build/tables/items'):
            os.mkdir(r'build/tables/items')
        with open(r'build/tables/items/vanilla_tags.md', 'w', encoding="utf-8") as f:
            f.write(ItemTagBuilder(self.itemTags).render())
        return ''
