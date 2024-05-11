
import json5, json
import os

from data_driven.builder import SchemaBuilder


class BlockceptionSchemaGenerator(object):
    def __init__(self):
        self.schemas = {}
        self.schemas['item'] = {}
        with open(r'assets/schemas-blockception/behavior/items/items.json', 'r', encoding="utf-8") as f:
            self.schemas['item']['behavior'] = (json5.load(f), r'assets/schemas-blockception/behavior/items')
        with open(r'assets/schemas-blockception/resource/items/items.json', 'r', encoding="utf-8") as f:
            self.schemas['item']['resource'] = (json5.load(f), r'assets/schemas-blockception/resource/items')
        self.schemas['block'] = {}
        with open(r'assets/schemas-blockception/behavior/blocks/blocks.json', 'r', encoding="utf-8") as f:
            self.schemas['block']['behavior'] = (json5.load(f), r'assets/schemas-blockception/behavior/blocks')
        with open(r'assets/schemas-blockception/resource/blocks.json', 'r', encoding="utf-8") as f:
            self.schemas['block']['resource'] = (json5.load(f), r'assets/schemas-blockception/resource')
        self.schemas['entity'] = {}
        with open(r'assets/schemas-blockception/behavior/entities/entities.json', 'r', encoding="utf-8") as f:
            self.schemas['entity']['behavior'] = (json5.load(f), r'assets/schemas-blockception/behavior/entities')
        with open(r'assets/schemas-blockception/behavior/entities/filters/filters.json', 'r', encoding="utf-8") as f:
            self.schemas['entity']['behavior/filter'] = (json5.load(f), r'assets/schemas-blockception/behavior/entities/filters')
        with open(r'assets/schemas-blockception/behavior/animations/animations.json', 'r', encoding="utf-8") as f:
            self.schemas['entity']['behavior/animation'] = (json5.load(f), r'assets/schemas-blockception/behavior/animations')
        with open(r'assets/schemas-blockception/behavior/animation_controllers/animation_controller.json', 'r', encoding="utf-8") as f:
            self.schemas['entity']['behavior/animation-controller'] = (json5.load(f), r'assets/schemas-blockception/behavior/animation_controllers')
        with open(r'assets/schemas-blockception/resource/entity/entity.json', 'r', encoding="utf-8") as f:
            self.schemas['entity']['resource'] = (json5.load(f), r'assets/schemas-blockception/resource/entity')
        with open(r'assets/schemas-blockception/resource/animations/actor_animation.json', 'r', encoding="utf-8") as f:
            self.schemas['entity']['resource/animation'] = (json5.load(f), r'assets/schemas-blockception/resource/animations')
        with open(r'assets/schemas-blockception/resource/animation_controllers/animation_controller.json', 'r', encoding="utf-8") as f:
            self.schemas['entity']['resource/animation-controller'] = (json5.load(f), r'assets/schemas-blockception/resource/animation_controllers')
        self.schemas['spawn-rule'] = {}
        with open(r'assets/schemas-blockception/behavior/spawn_rules/spawn_rules.json', 'r', encoding="utf-8") as f:
            self.schemas['spawn-rule']['definition'] = (json5.load(f), r'assets/schemas-blockception/behavior/spawn_rules')
        self.schemas['biome'] = {}
        with open(r'assets/schemas-blockception/behavior/biomes/biomes.json', 'r', encoding="utf-8") as f:
            self.schemas['biome']['behavior'] = (json5.load(f), r'assets/schemas-blockception/behavior/biomes')
        with open(r'assets/schemas-blockception/resource/biomes_client.json', 'r', encoding="utf-8") as f:
            self.schemas['biome']['resource'] = (json5.load(f), r'assets/schemas-blockception/resource')
        self.schemas['feature'] = {}
        with open(r'assets/schemas-blockception/behavior/features/features.json', 'r', encoding="utf-8") as f:
            self.schemas['feature']['definition'] = (json5.load(f), r'assets/schemas-blockception/behavior/features')
        self.schemas['feature-rule'] = {}
        with open(r'assets/schemas-blockception/behavior/feature_rules/feature_rules.json', 'r', encoding="utf-8") as f:
            self.schemas['feature-rule']['definition'] = (json5.load(f), r'assets/schemas-blockception/behavior/feature_rules')
        self.schemas['recipe'] = {}
        with open(r'assets/schemas-blockception/behavior/recipes/recipes.json', 'r', encoding="utf-8") as f:
            self.schemas['recipe']['definition'] = (json5.load(f), r'assets/schemas-blockception/behavior/recipes')
        self.schemas['loot-table'] = {}
        with open(r'assets/schemas-blockception/behavior/loot_tables/loot_tables.json', 'r', encoding="utf-8") as f:
            self.schemas['loot-table']['definition'] = (json5.load(f), r'assets/schemas-blockception/behavior/loot_tables')
        self.schemas['trading'] = {}
        with open(r'assets/schemas-blockception/behavior/trading/trading.json', 'r', encoding="utf-8") as f:
            self.schemas['trading']['definition'] = (json5.load(f), r'assets/schemas-blockception/behavior/trading')
        self.schemas['volume'] = {}
        with open(r'assets/schemas-blockception/behavior/volumes/volumes.json', 'r', encoding="utf-8") as f:
            self.schemas['volume']['definition'] = (json5.load(f), r'assets/schemas-blockception/behavior/volumes')
        self.schemas['dialogue'] = {}
        with open(r'assets/schemas-blockception/behavior/dialogue/dialogue.json', 'r', encoding="utf-8") as f:
            self.schemas['dialogue']['definition'] = (json5.load(f), r'assets/schemas-blockception/behavior/dialogue')
        self.schemas['function'] = {}
        with open(r'assets/schemas-blockception/behavior/functions/tick.json', 'r', encoding="utf-8") as f:
            self.schemas['function']['tick'] = (json5.load(f), r'assets/schemas-blockception/behavior/functions')
        self.schemas['fog'] = {}
        with open(r'assets/schemas-blockception/resource/fog/fog.json', 'r', encoding="utf-8") as f:
            self.schemas['fog']['definition'] = (json5.load(f), r'assets/schemas-blockception/resource/fog')
        self.schemas['particle'] = {}
        with open(r'assets/schemas-blockception/resource/particles/particles.json', 'r', encoding="utf-8") as f:
            self.schemas['particle']['definition'] = (json5.load(f), r'assets/schemas-blockception/resource/particles')
        self.schemas['block_culling'] = {}
        with open(r'assets/schemas-blockception/resource/block_culling/block_culling.json', 'r', encoding="utf-8") as f:
            self.schemas['block_culling']['definition'] = (json5.load(f), r'assets/schemas-blockception/resource/block_culling')
        self.schemas['attachable'] = {}
        with open(r'assets/schemas-blockception/resource/attachables/attachables.json', 'r', encoding="utf-8") as f:
            self.schemas['attachable']['definition'] = (json5.load(f), r'assets/schemas-blockception/resource/attachables')
        self.schemas['geometry'] = {}
        with open(r'assets/schemas-blockception/resource/models/entity/model_entity.json', 'r', encoding="utf-8") as f:
            self.schemas['geometry']['definition'] = (json5.load(f), r'assets/schemas-blockception/resource/models/entity')
        self.schemas['render_controller'] = {}
        with open(r'assets/schemas-blockception/resource/render_controllers/render_controllers.json', 'r', encoding="utf-8") as f:
            self.schemas['render_controller']['definition'] = (json5.load(f), r'assets/schemas-blockception/resource/render_controllers')
        self.schemas['material'] = {}
        with open(r'assets/schemas-blockception/resource/materials/materials.json', 'r', encoding="utf-8") as f:
            self.schemas['material']['definition'] = (json5.load(f), r'assets/schemas-blockception/resource/materials')
        self.schemas['sounds'] = {}
        with open(r'assets/schemas-blockception/resource/sounds/sound_definitions.json', 'r', encoding="utf-8") as f:
            self.schemas['sounds']['sound'] = (json5.load(f), r'assets/schemas-blockception/resource/sounds')
        with open(r'assets/schemas-blockception/resource/sounds/music_definitions.json', 'r', encoding="utf-8") as f:
            self.schemas['sounds']['music'] = (json5.load(f), r'assets/schemas-blockception/resource/sounds')
        self.schemas['texture'] = {}
        with open(r'assets/schemas-blockception/resource/textures/textures_list.json', 'r', encoding="utf-8") as f:
            self.schemas['texture']['texture-list'] = (json5.load(f), r'assets/schemas-blockception/resource/textures')
        with open(r'assets/schemas-blockception/resource/textures/texture_set.json', 'r', encoding="utf-8") as f:
            self.schemas['texture']['texture-set'] = (json5.load(f), r'assets/schemas-blockception/resource/textures')
        with open(r'assets/schemas-blockception/resource/textures/terrain_texture.json', 'r', encoding="utf-8") as f:
            self.schemas['texture']['terrain-texture'] = (json5.load(f), r'assets/schemas-blockception/resource/textures')
        with open(r'assets/schemas-blockception/resource/textures/item_texture.json', 'r', encoding="utf-8") as f:
            self.schemas['texture']['item-texture'] = (json5.load(f), r'assets/schemas-blockception/resource/textures')
        with open(r'assets/schemas-blockception/resource/textures/flipbook_textures.json', 'r', encoding="utf-8") as f:
            self.schemas['texture']['flipbook-texture'] = (json5.load(f), r'assets/schemas-blockception/resource/textures')
        with open(r'assets/schemas-blockception/resource/textures/ui_texture_definition.json', 'r', encoding="utf-8") as f:
            self.schemas['texture']['ui-texture'] = (json5.load(f), r'assets/schemas-blockception/resource/textures')
        self.schemas['ui'] = {}
        with open(r'assets/schemas-blockception/resource/ui/ui.json', 'r', encoding="utf-8") as f:
            self.schemas['ui']['definition'] = (json5.load(f), r'assets/schemas-blockception/resource/ui')
        with open(r'assets/schemas-blockception/resource/ui/_ui_defs.json', 'r', encoding="utf-8") as f:
            self.schemas['ui']['ui-definition'] = (json5.load(f), r'assets/schemas-blockception/resource/ui')
        with open(r'assets/schemas-blockception/resource/ui/_global_variables.json', 'r', encoding="utf-8") as f:
            self.schemas['ui']['global-variables'] = (json5.load(f), r'assets/schemas-blockception/resource/ui')

    def generate(self):
        if not os.path.exists(r'build'):
            os.mkdir(r'build')
        if not os.path.exists(r'build/data-driven'):
            os.mkdir(r'build/data-driven')
        if not os.path.exists(r'build/data-driven/blockception'):
            os.mkdir(r'build/data-driven/blockception')
        return generate(self, 'blockception/')


class BEDWSchemaGenerator(object):
    def __init__(self):
        self.schemas = {}
        self.schemas['item'] = {}
        with open(r'assets/schemas/behavior/items/item.json', 'r', encoding="utf-8") as f:
            self.schemas['item']['behavior'] = (json5.load(f), r'assets/schemas/behavior/items')
        self.schemas['block'] = {}
        with open(r'assets/schemas/behavior/blocks/block.json', 'r', encoding="utf-8") as f:
            self.schemas['block']['behavior'] = (json5.load(f), r'assets/schemas/behavior/blocks')
        self.schemas['entity'] = {}
        with open(r'assets/schemas/behavior/entities/entity.json', 'r', encoding="utf-8") as f:
            self.schemas['entity']['behavior'] = (json5.load(f), r'assets/schemas/behavior/entities')

    def generate(self):
        if not os.path.exists(r'build'):
            os.mkdir(r'build')
        if not os.path.exists(r'build/data-driven'):
            os.mkdir(r'build/data-driven')
        return generate(self)


def generate(cls, base=''):
    pageListText = ''
    for folder in cls.schemas:
        pageListText += '- {}:'.format(folderToName(folder)) + '\n'
        if not os.path.exists(r'build/data-driven/' + base + folder):
            os.mkdir(r'build/data-driven/' + base + folder)
        recordedFolders = []
        for s in cls.schemas[folder]:
            schema = cls.schemas[folder][s]
            s = s.split('/')
            builder = SchemaBuilder(schema[0], schema[1])
            if not os.path.exists(r'build/data-driven/{}{}/{}'.format(base, folder, s[0])):
                os.mkdir(r'build/data-driven/{}{}/{}'.format(base, folder, s[0]))
            with open(r'build/data-driven/{}{}/{}/{}.md'.format(base, folder, s[0], 'index' if len(s) == 1 else s[1]), 'w', encoding="utf-8") as f:
                f.write(builder.render())
            if s[0] not in recordedFolders:
                recordedFolders.append(s[0])
                name = schema[0].get('title', s[0])
                name = secondFolderToName(s[0], name)
                pageListText += '  - {}:'.format(name) + '\n'
            pageListText += '    - {}'.format(r'refs/data-driven/{}{}/{}/{}.md'.format(base, folder, s[0], 'index' if len(s) == 1 else s[1])) + '\n'
            pageList = []
            for c in builder.components:
                if not os.path.exists(r'build/data-driven/{}{}/{}/components'.format(base, folder, s[0])):
                    os.mkdir(r'build/data-driven/{}{}/{}/components'.format(base, folder, s[0]))
                with open(c[1], 'r', encoding="utf-8") as f:
                    data = json5.load(f)
                    componentBuilder = SchemaBuilder(data, os.path.dirname(c[1]))
                    componentBuilder.isComponent = True
                    with open(r'build/data-driven/{}{}/{}/components/{}.md'.format(base, folder, s[0], c[1].split('/')[-1].split('\\')[-1].replace('.json', '')), 'w', encoding="utf-8") as f:
                        f.write(componentBuilder.render())
                    pageList.append({'name': f'<code>{c[0]}</code>', 'path': 'refs/data-driven/{}{}/{}/components/{}.md'.format(base, folder, s[0], c[1].split('/')[-1].split('\\')[-1].replace('.json', ''))})
            if len(pageList) > 0:
                pageListText += '    - {}:'.format('组件') + '\n'
                pageListText += '      ' + '\n      '.join(['- {}: {}'.format(p['name'], p['path']) for p in pageList]) + '\n'
            pageList = []
            for c in builder.conditions:
                if not os.path.exists(r'build/data-driven/{}{}/{}/conditions'.format(base, folder, s[0])):
                    os.mkdir(r'build/data-driven/{}{}/{}/conditions'.format(base, folder, s[0]))
                with open(c[1], 'r', encoding="utf-8") as f:
                    data = json5.load(f)
                    componentBuilder = SchemaBuilder(data, os.path.dirname(c[1]))
                    componentBuilder.isComponent = True
                    with open(r'build/data-driven/{}{}/{}/conditions/{}.md'.format(base, folder, s[0], c[1].split('/')[-1].split('\\')[-1].replace('.json', '')), 'w', encoding="utf-8") as f:
                        f.write(componentBuilder.render())
                    pageList.append({'name': f'<code>{c[0]}</code>', 'path': 'refs/data-driven/{}{}/{}/conditions/{}.md'.format(base, folder, s[0], c[1].split('/')[-1].split('\\')[-1].replace('.json', ''))})
            if len(pageList) > 0:
                pageListText += '    - {}:'.format('条件') + '\n'
                pageList.sort(key=lambda x: x['name'])
                pageListText += '      ' + '\n      '.join(['- {}: {}'.format(p['name'], p['path']) for p in pageList]) + '\n'
    return pageListText

def folderToName(folder):
    if folder == 'item':
        return '物品'
    elif folder == 'block':
        return '方块'
    elif folder == 'entity':
        return '实体'
    elif folder == 'spawn-rule':
        return '生成规则'
    elif folder == 'biome':
        return '生物群系'
    elif folder == 'feature':
        return '地物'
    elif folder == 'feature-rule':
        return '地物规则'
    elif folder == 'recipe':
        return '配方'
    elif folder == 'loot-table':
        return '战利品表'
    elif folder == 'trading':
        return '交易'
    elif folder == 'volume':
        return '功能域'
    elif folder == 'dialogue':
        return '对话'
    elif folder == 'function':
        return '函数'
    elif folder == 'fog':
        return '迷雾'
    elif folder == 'particle':
        return '粒子'
    elif folder == 'block_culling':
        return '方块剔除'
    elif folder == 'attachable':
        return '附着物'
    elif folder == 'geometry':
        return '几何'
    elif folder == 'render_controller':
        return '渲染控制器'
    elif folder == 'material':
        return '材质'
    elif folder == 'sounds':
        return '声音'
    elif folder == 'texture':
        return '纹理'
    elif folder == 'ui':
        return 'UI'
    return folder

def secondFolderToName(folder, default):
    if folder == 'behavior':
        return '行为定义'
    elif folder == 'resource':
        return '资源定义'
    elif folder == 'definition':
        return '定义'
    elif folder == 'tick':
        return '滴答'
    elif folder == 'sound':
        return '音效'
    elif folder == 'music':
        return '音乐'
    elif folder == 'texture-list':
        return '纹理列表'
    elif folder == 'texture-set':
        return '纹理集'
    elif folder == 'terrain-texture':
        return '方块纹理'
    elif folder == 'item-texture':
        return '物品纹理'
    elif folder == 'flipbook-texture':
        return '翻书纹理'
    elif folder == 'ui-texture':
        return 'UI纹理'
    elif folder == 'ui-definition':
        return '文件列表'
    elif folder == 'global-variables':
        return '全局变量'
    return default