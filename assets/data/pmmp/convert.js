const fs = require('fs')
const nbt = require('prismarine-nbt')

async function convert(file) {
  const buffer = fs.readFileSync(file)
  const { parsed, type } = await nbt.parse(buffer)
  fs.createWriteStream(file.replace('.nbt', '.converted.nbt')).write(nbt.writeUncompressed(parsed, "little")) // Write it back
}

convert('biome_definitions.nbt')
convert('biome_definitions_full.nbt')
convert('canonical_block_states.nbt')
convert('entity_identifiers.nbt')