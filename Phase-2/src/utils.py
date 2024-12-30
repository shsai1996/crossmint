def print_megaverse(objects):
	"""Prints the details of the created megaverse objects

	Args:
		objects (list): The list of the created megaverse objects. This list can
			be retrieved from the return value of the create_megaverse function.
	"""
	print("MEGAVERSE:")
	for object in objects:
		print(f"{object.__class__.__name__}: row {object.row} | column {object.column}")

def print_goal_map(goal_map):
	"""Prints the received goal_map

	Args:
		goal_map (dict): The current goal_map of the candidate
	"""
	print("GOAL MAP:", goal_map)