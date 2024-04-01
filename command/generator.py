import json
import os

from command.builder import CommandBuilder


class CommandGenerator(object):
    def __init__(self):
        self.commands = {}
        self.enums = {}
        self.enumMaps = {}
        self.commandList = {}
        self.extraCommands = {}
        with open(r'assets/docs/command_modules/mojang-commands-internal.json', 'r') as f:
            self.commands = json.load(f)
        with open(r'assets/data/command_arg_types_full_v.json', 'r') as f:
            self.enumMaps = json.load(f)
        for enum in self.commands['command_enums']:
            self.enums[enum['name'].upper()] = enum
        for command in self.commands['commands']:
            self.commandList[command['name']] = command
        with open(r'assets/extra/command/additional_commands.json', 'r') as f:
            self.extraCommands = json.load(f)
        self.mergeCommands()


    def generate(self):
        pageList = []
        for c in self.commandList:
            command = self.commandList[c]
            builder = CommandBuilder(command, self.enums, self.enumMaps)
            if not os.path.exists(r'build/commands'):
                os.mkdir(r'build/commands')
            with open(r'build/commands/{}.md'.format(command["name"]), 'w', encoding="utf-8") as f:
                f.write(builder.render())
            pageList.append({'name': command["name"], 'path': 'refs/commands/{}.md'.format(command["name"])})
        pageList.sort(key=lambda x: x['name'])
        pageListText = '\n'.join(['- <code>{}</code>: {}'.format(p['name'], p['path']) for p in pageList])
        return pageListText

    def mergeCommands(self):
        for e in self.extraCommands["command_enums"]:
            if e["name"].upper() not in self.enums:
                self.enums[e["name"].upper()] = e
            else:
                self.enums[e["name"].upper()]["values"].extend(e["values"])
        for c in self.extraCommands["commands"]:
            if c["name"] not in self.commandList:
                self.commandList[c["name"]] = c
            else:
                overloadsDict = {}
                for o in self.commandList[c["name"]]["overloads"]:
                    overloadsDict[o["name"]] = o
                for o in c["overloads"]:
                    if o["name"] not in overloadsDict:
                        overloadsDict[o["name"]] = o
                    else:
                        overloadsDict[o["name"]].update(o)
                overloads = []
                for o in overloadsDict:
                    overloads.append(overloadsDict[o])
                overloads.sort(key=lambda x: int(x["name"]))
                self.commandList[c["name"]].update(c)
                self.commandList[c["name"]]["overloads"] = overloads