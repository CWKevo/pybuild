A crappy Minecraft clone with bad performance, yet kinda-working schematic and mapdata system.

What works:
- [X] - Camera, rotating sky
- [X] - Placing/breaking various blocks
- [X] - Very basic, inbuilt collisions & movement system
- [X] - Very basic writing and loading map data (JSON)
- [X] - Very basic schematic system (same as map data, but relative to block position)
    - [ ] - Overwrite old blocks when placing schematic (remove old and add new ones)

What I would like to do with this project:
- [ ] - Better movement system & collisions - important (right now, player can pass through ceiling)
- [ ] - Improve performance with many blocks on the screen: meshes could probably do this.
    - If perfomance is bad, I cannot move further - top priority!
- [ ] - Working chunk implementation: load only parts of the world at a time
- [ ] - Save chunks to map data - split into different files for each chunk (maybe zipping/unzipping for big data?)
  - Problem - how to remove existing blocks in JSON data? Would need to do some filtering and looping through entire list - performance killer (for bigger data) 
- [ ] - More blocks
- [ ] - Items
- [ ] - Healthbar
- [ ] - Entities
