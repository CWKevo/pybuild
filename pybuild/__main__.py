from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

import os
import json
import pathlib
BASE_PATH = pathlib.Path(__file__).parent.absolute()

app = Ursina()

sky_texture = load_texture(name='skybox.png')
print(sky_texture)

block_textures = {}
for block in os.listdir(Path(f"{BASE_PATH}/assets")):
	if block.endswith("_block.png"):
		block_name = block.replace(".png", '')
		print(block, block_name)

		block_textures[f"{block_name}"] = load_texture(name=block_name)

print(block_textures)

block_pick = 1


class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = block_textures["grass_block"]):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
			scale = 0.5)

	def input(self, key):
		if self.hovered:
			if key == 'right mouse down':
				if block_pick == 1:
					place_block(id="grass_block", position=self.position + mouse.normal)
				elif block_pick == 2:
					place_block(id="stone_block", position=self.position + mouse.normal)
				elif block_pick == 3:
					place_block(id="brick_block", position=self.position + mouse.normal)
				elif block_pick == 4:
					place_block(id="dirt_block", position=self.position + mouse.normal)

			if key == 'left mouse down':
				remove_block(position=(self.x, self.y, self.z))
				destroy(self)

			if key == 's':
				load_schematic(self)


class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 200,
			double_sided = True,
			eternal = True)


class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = load_texture('arm_texture.png'),
			scale = 0.2,
			rotation = Vec3(150,-10,0),
			position = Vec2(0.4,-0.6),
			eternal = True)


def place_block(id: int, position: Vec3, write=True):
	"""
		Places a block and saves it to map_data.json.
		Destroys block that already is on this position.
	"""
	with open(f"{BASE_PATH}/data/map_data.json", "r") as md:
		map_data = json.load(md) # type: list
		print("Obtained block data from JSON")

	block_data = [id, position[0], position[1], position[2]]

	if block_data in map_data:
		print("Block exists, removing.")
		remove_block((block_data[1], block_data[2], block_data[3]))

	print("Appened block data & created voxel")
	map_data.append(block_data)
	Voxel(position=(position[0], position[1], position[2]), texture=block_textures[id])

	if write:
		with open(f"{BASE_PATH}/data/map_data.json", "w") as md:
			md.write(json.dumps(map_data))
			print("Wrote block data to JSON")


def remove_block(position: Vec3):
	"""Removes a block in map_data.json"""
	with open(f"{BASE_PATH}/data/map_data.json", "r") as md:
		map_data = json.load(md) # type: list
		print("Obtained block data from JSON")

	for block in map_data:
		if block[1] == position[0] and block[2] == position[1] and block[3] == position[2]:
			map_data.remove(block)
			block = Entity(add_to_scene_entities=False, position=(block[1], block[2], block[3]))
			destroy(block)
			print("Found block, removed")

	with open(f"{BASE_PATH}/data/map_data.json", "w") as md:
		md.write(json.dumps(map_data))
		print("Wrote map data")


def regenerate_world():
	"""Re-generates the world"""
	scene.clear()

	for z in range(20):
		for x in range(20):
			place_block(id="grass_block", position=(x, 0, z))
			print("Behold my block-refreshing powers!")
	
	print("I did it... I refreshed the world!")


def load_map_data():
	"""Refreshes the world/loads map data."""
	with open(f"{BASE_PATH}/data/map_data.json", "r") as map_data:
		map_data = json.load(map_data)
		print("Loaded map data for schematic")

	for block in map_data:
		place_block(id=block[0], position=(block[1], block[2], block[3]), write=False)


def load_schematic(obj: Voxel):
	"""Loads a schematic from schematic.json"""
	with open(f"{BASE_PATH}/data/schematic.json", "r") as schem:
		schem_data = json.load(schem) # type: list

	for block in schem_data:
		block_position = (obj.x + block[1], obj.y + block[2], obj.z + block[3])
		place_block(id=block[0], position=block_position)


# Initialize entities:
player = FirstPersonController()
player.eternal = True
sky = Sky()
hand = Hand()


# Load saved map data:
load_map_data()


# Main loop:
def update():
	# Prevent player from falling out of the world infinitely:
	if player.y < -50:
		player.y = 20


	# Sky rotation:
	sky.position = player.position
	sky.rotation_y += 0.025


	# Handle block choosing:
	global block_pick

	if held_keys['1']:
		block_pick = 1
	elif held_keys['2']:
		block_pick = 2
	elif held_keys['3']:
		block_pick = 3
	elif held_keys['4']:
		block_pick = 4


	# Reloads the world:
	if held_keys['r']:
		scene.clear()
		load_map_data()


	# Regenerates the world, overwriting existing save:
	if held_keys['x']:
		regenerate_world()

	# Exit game, if ESC is pressed:
	if held_keys['esc']:
		app.userExit()


if __name__ == "__main__":
	app.run()
