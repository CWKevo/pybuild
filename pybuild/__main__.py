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
					Voxel(position = self.position + mouse.normal, texture = block_textures["grass_block"])
				elif block_pick == 2:
					Voxel(position = self.position + mouse.normal, texture = block_textures["stone_block"])
				elif block_pick == 3:
					Voxel(position = self.position + mouse.normal, texture = block_textures["brick_block"])
				elif block_pick == 4:
					Voxel(position = self.position + mouse.normal, texture = block_textures["dirt_block"])
				Wait(1)

			if key == 'left mouse down':
				destroy(self)
				Wait(1)

			if key == 'x':
				load_schematic(self)


class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 200,
			double_sided = True)


class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = load_texture('arm_texture.png'),
			scale = 0.2,
			rotation = Vec3(150,-10,0),
			position = Vec2(0.4,-0.6))


def write_map_data():
	map_data = {"data": []}

	for z in range(20):
		for x in range(20):
			map_data["data"].append(["grass_block", x, 0, z])

	with open(f"{BASE_PATH}/map_data.json", "w") as md:
		json.dump(map_data, md)


def load_map_data():
	with open(f"{BASE_PATH}/map_data.json", "r") as map_data:
		map_data = json.load(map_data)
	
	for block in map_data["data"]:
		Voxel(position=(block[1], block[2], block[3]), texture=block_textures[block[0]])


def load_schematic(obj):
	with open(f"{BASE_PATH}/schematic.json", "r") as schem:
		schem_data = json.load(schem)

	for block in schem_data["data"]:
		Voxel(position=(obj.x + block[1], obj.y + block[2], obj.z + block[3]), texture=block_textures[block[0]])

load_map_data()


player = FirstPersonController()
sky = Sky()
hand = Hand()

def update():
	sky.position = player.position
	sky.rotation_y += 0.025
	global block_pick

	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4

if __name__ == "__main__":
	app.run()
