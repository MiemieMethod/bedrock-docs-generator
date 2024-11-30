from markdown.writer import *

import os
import json5, json

class SchemaBuilder(MarkdownWriter):

    def __init__(self, convertedSchema, path, name):
        super().__init__()
        self.entry = convertedSchema
        self.basePath = path
        self.name = name
        self.components = []
        self.conditions = []
        self.isComponent = False

        self.validFormatVersions = [
            SemVersion('0.1.0'),
            SemVersion('1.0.0'),
            SemVersion('1.1.0'),
            SemVersion('1.2.0'),
            SemVersion('1.3.0'),
            SemVersion('1.4.0'),
            SemVersion('1.5.0'),
            SemVersion('1.6.0'),
            SemVersion('1.7.0'),
            SemVersion('1.8.0'),
            SemVersion('1.9.0'),
            SemVersion('1.10.0'),
            SemVersion('1.11.0'),
            SemVersion('1.12.0'),
            SemVersion('1.13.0'),
            SemVersion('1.14.0'),
            SemVersion('1.15.0'),
            SemVersion('1.16.0'),
            SemVersion('1.16.100'),
            SemVersion('1.16.200'),
            SemVersion('1.16.210'),
            SemVersion('1.16.220'),
            SemVersion('1.16.230'),
            SemVersion('1.17.0'),
            SemVersion('1.17.10'),
            SemVersion('1.17.20'),
            SemVersion('1.17.30'),
            SemVersion('1.17.40'),
            SemVersion('1.18.0'),
            SemVersion('1.18.10'),
            SemVersion('1.18.20'),
            SemVersion('1.18.30'),
            SemVersion('1.19.0'),
            SemVersion('1.19.10'),
            SemVersion('1.19.20'),
            SemVersion('1.19.30'),
            SemVersion('1.19.40'),
            SemVersion('1.19.50'),
            SemVersion('1.19.60'),
            SemVersion('1.19.70'),
            SemVersion('1.19.80'),
            SemVersion('1.20.0'),
            SemVersion('1.20.10'),
            SemVersion('1.20.20'),
            SemVersion('1.20.30'),
            SemVersion('1.20.40'),
            SemVersion('1.20.50'),
            SemVersion('1.20.60'),
            SemVersion('1.20.70'),
            SemVersion('1.20.80'),
            SemVersion('1.21.0'),
            SemVersion('1.21.10'),
            SemVersion('1.21.20'),
            SemVersion('1.21.30'),
            SemVersion('1.21.40'),
            SemVersion('1.21.50'),
            SemVersion('1.21.60'),
        ]

    def preRender(self):
        version = '1.21.60.21'
        title = self.entry.get('title', self.name)
        self.addHeading(title, 1)
        self.addBlockquote('文档版本：{}'.format(version))
        self.addText(self.entry.get('description', ''))
        self.addHeading('结构', 2)
        self.addText(self.buildNode('', self.entry, self.basePath, 3, True))


    def render(self):
        return super().render()

    def buildNode(self, key, node, basePath, level=3, newFile=False):
        rootVersionRange = VersionRange(node.get('version', [{'min': '0.0.0', 'max': '*'}]))
        rootDeprecatedRange = VersionRange(node.get('deprecated', [{'value': '0.0.0'}]))
        rootExperimentRange = VersionRange(node.get('experiment', [{'value': '0.0.0'}]))
        writer = MarkdownWriter()
        cache = ''
        for version in self.validFormatVersions:
            if rootVersionRange.greaterThan(version):
                continue
            if version not in rootVersionRange:
                if version in rootDeprecatedRange:
                    text = MarkdownWriter().addAdmonition('已弃用', '当前对象已在此版本中弃用，即使能正常解析也无法正常发挥功能。', 'warning', level + 1).render()
                    text += self.buildTreeData(node, key, rootVersionRange, rootDeprecatedRange, rootExperimentRange, version, level)
                else:
                    text = MarkdownWriter().addAdmonition('已移除', '当前对象已在此版本中移除，无法正常解析。', 'danger', level + 1).render()
            else:
                text = self.buildTreeData(node, key, rootVersionRange, rootDeprecatedRange, rootExperimentRange, version, level)
            if text != cache:
                writer.addTab(version.version, text, level)
                cache = text
        return writer.render()

    def buildTreeData(self, node, key, ver, dep, exp, formatVer, level=0):
        treeData = [['object', key, '根对象。', 0, True]]
        self.parseChildren(node, treeData, ver, dep, exp, formatVer, 1)
        text = self.createTreeView(treeData, level + 1)
        return text

    def parseChildren(self, node, data, ver, dep, exp, formatVer, lvl=0):
        children = node['children']
        for child in children:
            newver = VersionRange(child[2]['version']) if 'version' in child[2] else ver
            newdep = VersionRange(child[2]['deprecated']) if 'deprecated' in child[2] else dep
            newexp = VersionRange(child[2]['experiment']) if 'experiment' in child[2] else exp
            if formatVer not in newver and formatVer not in newdep:
                continue
            type = child[0]
            if type == 'recursive':
                type = 'null'
            if type == 'enum':
                type = 'string'
            key = child[1]
            if key == '<any array element>':
                key = ''
            if key == '<any object property>':
                key = '<*任意键名*>'
            desc = ''
            if formatVer in newexp:
                desc += '<!-- md:flag experimental -->'
            data.append([type, key, desc, lvl, child[2].get('required', False)])
            if type == 'object' or type == 'array':
                self.parseChildren(child[2], data, newver, newdep, newexp, formatVer, lvl + 1)


    def createTreeView(self, data: list[list], level=3):
        text = ""
        for item in data:
            if isinstance(item, list):
                type = item[0]
                key = item[1]
                desc = item[2]
                lvl = item[3]
                req = item[4]
                text += f"{lvl * '    '}- {{{{json|{type}|{key}{'|required=1' if req else ''}}}}}：{desc}\n"
        writer = MarkdownWriter()
        writer.addHtmlBlock('div.treeview', text, level)
        return writer.render()


class SemVersion:
    def __init__(self, version: str):
        self.version = version
        major, minor, patch = self.version.split('.')
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)

    def __lt__(self, other):
        if self.major < other.major:
            return True
        elif self.major == other.major:
            if self.minor < other.minor:
                return True
            elif self.minor == other.minor:
                if self.patch < other.patch:
                    return True
        return False

    def __gt__(self, other):
        if self.major > other.major:
            return True
        elif self.major == other.major:
            if self.minor > other.minor:
                return True
            elif self.minor == other.minor:
                if self.patch > other.patch:
                    return True
        return False

    def __eq__(self, other):
        return self.version == other.version

    def __ne__(self, other):
        return self.version != other.version

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __str__(self):
        return self.version

    def __repr__(self):
        return f"SemVersion('{self.version}')"

    def __hash__(self):
        return hash(self.version)

    def __iter__(self):
        return iter([self.major, self.minor, self.patch])

    def __getitem__(self, index):
        return [self.major, self.minor, self.patch][index]

    def __setitem__(self, index, value):
        if index == 0:
            self.major = value
        elif index == 1:
            self.minor = value
        elif index == 2:
            self.patch = value
        else:
            raise IndexError("Index out of range")

    def bump(self, index):
        if index == 0:
            self.major += 1
            self.minor = 0
            self.patch = 0
        elif index == 1:
            self.minor += 1
            self.patch = 0
        elif index == 2:
            self.patch += 1
        else:
            raise IndexError("Index out of range")

    def bumpMajor(self):
        self.bump(0)

    def bumpMinor(self):
        self.bump(1)

    def bumpPatch(self):
        self.bump(2)

    def toTuple(self):
        return


class VersionRange:
    def __init__(self, rangeDict):
        self.intervals = []
        for interval in rangeDict:
            self.intervals.append(VersionInterval(interval))

    def __contains__(self, version: SemVersion):
        for interval in self.intervals:
            if version in interval:
                return True
        return False

    def __str__(self):
        return ', '.join(str(interval) for interval in self.intervals)

    def __repr__(self):
        return f"VersionRange({str(self)})"

    def lessThan(self, version: SemVersion):
        result = True
        for interval in self.intervals:
            if not interval.lessThan(version):
                result = False
        return result

    def greaterThan(self, version: SemVersion):
        result = True
        for interval in self.intervals:
            if not interval.greaterThan(version):
                result = False
        return result


class VersionInterval:
    def __init__(self, intervalDict):
        if 'value' in intervalDict:
            self.min = SemVersion(intervalDict['value'])
            self.max = SemVersion(intervalDict['value'])
            self.min_exclusive = False
            self.max_exclusive = False
        else:
            self.min = SemVersion(intervalDict.get('min', '0.0.0'))
            self.max = SemVersion(intervalDict.get('max', '*')) if intervalDict.get('max', '*') != '*' else SemVersion('999.999.999')
            self.min_exclusive = intervalDict.get('min_exclusivity', False)
            self.max_exclusive = intervalDict.get('max_exclusivity', False)
        self.min_inclusive = not self.min_exclusive
        self.max_inclusive = not self.max_exclusive

    def __contains__(self, version: SemVersion):
        print(f'verify if version {version} is in interval {self}') if version == SemVersion('1.20.50') else None
        if self.min < version < self.max:
            print(f'{self.min} < {version} < {self.max}') if version == SemVersion('1.20.50') else None
            return True
        if self.min == version and self.min_inclusive:
            print(f'{self.min} == {version} and {self.min_inclusive}') if version == SemVersion('1.20.50') else None
            return True
        if self.max == version and self.max_inclusive:
            print(f'{self.max} == {version} and {self.max_inclusive}') if version == SemVersion('1.20.50') else None
            return True
        print(f'not') if version == SemVersion('1.20.50') else None
        return False

    def __str__(self):
        return f"{'(' if self.min_exclusive else '['}{self.min}, {self.max}{')' if self.max_exclusive else ']'}"

    def __repr__(self):
        return f"VersionInterval({str(self)})"

    def __eq__(self, other):
        return self.min == other.min and self.max == other.max and self.min_exclusive == other.min_exclusive and self.max_exclusive == other.max_exclusive

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.min, self.max, self.min_exclusive, self.max_exclusive))

    def __iter__(self):
        return iter([self.min, self.max])

    def __getitem__(self, index):
        return [self.min, self.max][index]

    def __setitem__(self, index, value):
        if index == 0:
            self.min = value
        elif index == 1:
            self.max = value
        else:
            raise IndexError("Index out of range")

    def lessThan(self, version: SemVersion):
        if self.max_inclusive and self.max < version:
            return True
        if not self.max_inclusive and self.max <= version:
            return True

    def greaterThan(self, version: SemVersion):
        if self.min_inclusive and self.min > version:
            return True
        if not self.min_inclusive and self.min >= version:
            return True