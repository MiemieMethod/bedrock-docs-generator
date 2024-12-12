const fs = require('fs')
const nbt = require('prismarine-nbt')

async function convert(file) {
  const buffer = fs.readFileSync(file)
  const { parsed, type } = await nbt.parse(buffer)
  fs.createWriteStream(file.replace('.nbt', '.converted.nbt')).write(nbt.writeUncompressed(parsed, "big")) // Write it back
}

convert('./allay/biome_definitions.nbt')
convert('./pmmp/biome_definitions.nbt')
convert('./pmmp/biome_definitions_full.nbt')
convert('./pmmp/canonical_block_states.nbt')
convert('./pmmp/entity_identifiers.nbt')