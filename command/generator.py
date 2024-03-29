import json
import os

from command.builder import CommandBuilder


class CommandGenerator(object):
    def __init__(self):
        self.commands = {}
        self.enums = {}
        self.enumMaps = {}
        with open(r'assets/docs/command_modules/mojang-commands-internal.json', 'r') as f:
            self.commands = json.load(f)
        with open(r'assets/data/command_arg_types_full_v.json', 'r') as f:
            self.enumMaps = json.load(f)
        for enum in self.commands['command_enums']:
            self.enums[enum['name'].upper()] = enum

    def generate(self):
        pageListText = ''
        for c in self.commands['commands']:
            command = c
            builder = CommandBuilder(command, self.enums, self.enumMaps)
            if not os.path.exists(r'build/commands'):
                os.mkdir(r'build/commands')
            with open(r'build/commands/{}.md'.format(command["name"]), 'w', encoding="utf-8") as f:
                f.write(builder.render())
            pageListText += '- <code>{}</code>: refs/commands/{}.md\n'.format(command["name"], command["name"])
        return pageListText