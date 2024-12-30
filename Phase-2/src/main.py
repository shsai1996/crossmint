import time
from api_interactions import get_env_variable, ApiClient
from astral_objects import Polyanet, Soloon, Cometh
from utils import print_megaverse, print_goal_map


def create_megaverse(api_client, goal_map):
	"""Creates the expected megaverse based on the specified goal map

	Args:
		api_client(ApiClient): The client to interact with the API
		goal_map (dict): The goal map that contains the expected megaverse

	Returns:
		list: A list of created megaverse objects
	"""
	megaverse_objects = []
	for row_index, row in enumerate(goal_map['goal']):
		for col_index, value in enumerate(row):
			if value == 'POLYANET':
				megaverse_objects.append(Polyanet(row_index, col_index))
			elif value.endswith('SOLOON'):
				color = value.split('_')[0].lower()
				megaverse_objects.append(Soloon(row_index, col_index, color))
			elif value.endswith('COMETH'):
				direction = value.split('_')[0].lower()
				megaverse_objects.append(Cometh(row_index, col_index, direction))
	
	for object in megaverse_objects:
		object.create(api_client)
		time.sleep(0.5)

	return megaverse_objects

def main():
	"""Main function to run the application

	Retrieves environment variables, initializes the API Client,
	retrieves the goal map, and creates the megaverse.
	"""
	candidate_id = get_env_variable('CANDIDATE_ID')
	base_url = get_env_variable('API_URL')
	api_client = ApiClient(base_url, candidate_id)

	goal_map = api_client.get_goal_map()
	if goal_map:
		objects = create_megaverse(api_client, goal_map)

if __name__ == "__main__":
	main()