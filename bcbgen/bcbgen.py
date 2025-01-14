import json
import os
import shutil

BLOCKS = [('minecraft:dirt', 'dirt', 'Block of Dirt'),
          ('minecraft:stone', 'stone', 'Block of Stone'),
          ('minecraft:deepslate', 'deepslate', 'Block of Deepslate'),
          ('minecraft:netherrack', 'netherrack', 'Block of Netherrack'),
          ('minecraft:end_stone', 'end_stone', 'Block of End Stone'),
          ('minecraft:coal_block', 'coal_block', 'Block of Coal'),
          ('minecraft:copper_block', 'copper_block', 'Block of Copper'),
          ('minecraft:iron_block', 'iron_block', 'Block of Iron'),
          ('minecraft:gold_block', 'gold_block', 'Block of Gold'),
          ('minecraft:diamond_block', 'diamond_block', 'Block of Diamond'),
          ('minecraft:emerald_block', 'emerald_block', 'Block of Emerald'),
          ('architects_palette:unobtanium_block', 'unobtanium_block', 'Block of Unobtanium')]

def SAMPLE(name):
    with open(f'./samples/{name}', 'rb' if name.endswith('.png') else 'r') as f:
        return f.read()

if os.path.isdir('./gen'):
    shutil.rmtree('./gen')
os.mkdir('./gen')

os.mkdir('./gen/src')
os.mkdir('./gen/src/main')
os.mkdir('./gen/src/main/java')
os.mkdir('./gen/src/main/java/com')
os.mkdir('./gen/src/main/java/com/benchmark')
os.mkdir('./gen/src/main/java/com/benchmark/bcb')
os.mkdir('./gen/src/main/resources')
os.mkdir('./gen/src/main/resources/assets')
os.mkdir('./gen/src/main/resources/assets/bcb')
os.mkdir('./gen/src/main/resources/assets/bcb/blockstates')
os.mkdir('./gen/src/main/resources/assets/bcb/lang')
os.mkdir('./gen/src/main/resources/assets/bcb/models')
os.mkdir('./gen/src/main/resources/assets/bcb/models/block')
os.mkdir('./gen/src/main/resources/assets/bcb/models/item')
os.mkdir('./gen/src/main/resources/assets/bcb/textures')
os.mkdir('./gen/src/main/resources/assets/bcb/textures/block')
os.mkdir('./gen/src/main/resources/data')
os.mkdir('./gen/src/main/resources/data/bcb')
os.mkdir('./gen/src/main/resources/data/bcb/loot_tables')
os.mkdir('./gen/src/main/resources/data/bcb/loot_tables/blocks')
os.mkdir('./gen/src/main/resources/data/bcb/recipes')
os.mkdir('./gen/src/main/resources/data/minecraft')
os.mkdir('./gen/src/main/resources/data/minecraft/tags')
os.mkdir('./gen/src/main/resources/data/minecraft/tags/blocks')
os.mkdir('./gen/src/main/resources/data/minecraft/tags/blocks/mineable')
os.mkdir('./gen/src/main/resources/META-INF')

# Fixed sample files

with open('./gen/src/main/resources/pack.mcmeta', 'w') as f:
    f.write(SAMPLE('pack.mcmeta'))
with open('./gen/src/main/resources/META-INF/mods.toml', 'w') as f:
    f.write(SAMPLE('mods.toml'))
for i in range(1, 10):
    with open(f'./gen/src/main/resources/assets/bcb/textures/block/layer_{i}.png', 'wb') as f:
        f.write(SAMPLE(f'layer_{i}.png'))

# Code

with open('./gen/src/main/java/com/benchmark/bcb/CompressedBlocks.java', 'w') as f:
    f.write(SAMPLE('code1.java'))
    for block_tuple in BLOCKS:
        block_id = block_tuple[1]
        for i in range(1, 10):
            f.write(f'	public static final RegistryObject<Block> {block_id.upper()}_{i} = BLOCKS.register("{block_id}_{i}", () -> new Block(Block.Properties.of().strength(5.0F, 10.0F).sound(SoundType.STONE).requiresCorrectToolForDrops()));\n')
            f.write(f'	public static final RegistryObject<Item> {block_id.upper()}_{i}_ITEM = ITEMS.register("{block_id}_{i}", () -> new BlockItem({block_id.upper()}_{i}.get(), new Item.Properties()));\n')
    f.write(SAMPLE('code2.java'))
    for block_tuple in BLOCKS:
        block_id = block_tuple[1]
        for i in range(1, 10):
            f.write(f'			event.accept({block_id.upper()}_{i}_ITEM);\n')
    f.write(SAMPLE('code3.java'))

# Other single files

with open('./gen/src/main/resources/assets/bcb/lang/en_us.json', 'w') as f:
    lang_dict = {}
    for block_tuple in BLOCKS:
        _, block_id, block_name = block_tuple
        for i in range(1, 10):
            k = f'block.bcb.{block_id}_{i}'
            v = f'{i}x ' if i > 1 else ''
            v += f'Compressed {block_name}'
            lang_dict[k] = v
    json.dump(lang_dict, f)
with open('./gen/src/main/resources/data/minecraft/tags/blocks/mineable/pickaxe.json', 'w') as f:
    tag_list = []
    for block_tuple in BLOCKS:
        block_id = block_tuple[1]
        for i in range(1, 10):
            tag_list.append(f'bcb:{block_id}_{i}')
    json.dump({'replace': False, 'values': tag_list}, f)

# Multiple files (per block)

for block_tuple in BLOCKS:
    block_item, block_id, block_name = block_tuple

    for i in range(1, 10):
        with open(f'./gen/src/main/resources/assets/bcb/blockstates/{block_id}_{i}.json', 'w') as f:
            json.dump({'variants': {'': {'model': f'bcb:block/{block_id}_{i}'}}}, f)
        with open(f'./gen/src/main/resources/assets/bcb/models/block/{block_id}_{i}.json', 'w') as f:
            bi = block_item.split(':')
            if bi[0] == 'minecraft':
                block_model_id = f'block/{bi[1]}'
            else:
                block_model_id = f'{bi[0]}:block/{bi[1]}'
            json.dump({
  'parent': block_model_id,
  'children': {
    'solid': {
      'parent': block_model_id,
      'render_type': 'minecraft:solid'
    },
    'translucent': {
      'parent': 'minecraft:block/cube_all',
      'render_type': 'minecraft:translucent',
      'textures': {
        'all': f'bcb:block/layer_{i}'
      }
    }
  },
  'item_render_order': [
    'solid',
    'translucent'
  ],
  'loader': 'forge:composite'
}, f)
        with open(f'./gen/src/main/resources/assets/bcb/models/item/{block_id}_{i}.json', 'w') as f:
            json.dump({'parent': f'bcb:block/{block_id}_{i}'}, f)
        with open(f'./gen/src/main/resources/data/bcb/loot_tables/blocks/{block_id}_{i}.json', 'w') as f:
            json.dump({'type': 'minecraft:block', 'pools': [{'name': 'default', 'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': f'bcb:{block_id}_{i}'}], 'conditions': [{'condition': 'minecraft:survives_explosion'}]}]}, f)
        with open(f'./gen/src/main/resources/data/bcb/recipes/{block_id}_{i}.json', 'w') as f:
            input_item = block_item if i == 1 else f'bcb:{block_id}_{i - 1}'
            output_item = f'bcb:{block_id}_{i}'
            json.dump({'type': 'crafting_shaped', 'pattern': ['BBB', 'BBB', 'BBB'], 'key': {'B': {'item': input_item}}, 'result': {'item': output_item}}, f)
        with open(f'./gen/src/main/resources/data/bcb/recipes/{block_id}_{i}_rev.json', 'w') as f:
            input_item = f'bcb:{block_id}_{i}'
            output_item = block_item if i == 1 else f'bcb:{block_id}_{i - 1}'
            json.dump({'type': 'crafting_shapeless', 'ingredients': [{'item': input_item}], 'result': {'item': output_item, 'count': 9}}, f)
