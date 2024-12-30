from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()

def get_env_variable(name):
	"""Retrieve the value of the specified environment variable needed by ApiClient

	Args:
		name (str): The name of the environment variable

	Returns:
		str: The value of the environment variable

	Raises: 
		ValueError: If the environment variable is not found or is empty
	"""
	value = os.getenv(name)
	if value is None:
		raise ValueError(f"No variable named {name} found in the .env file")
	elif value == "":
		raise ValueError(f"The value for {name} is empty in the .env file")
	return value

class ApiClient:
	"""Class for interacting with the megaverse API"""

	def __init__(self, base_url, candidate_id):
		"""
		Initializes the ApiClient

		Args:
			base_url (str): The base URL for the API
			candidate_id (str): The candidate ID for the API
		"""
		self.base_url = base_url
		self.candidate_id = candidate_id

	def create_polyanet(self, row, column):
		"""Creates a POLYANET at the given row and column

		Args:
			row (int): The row position
			column (int): The column position
		"""
		url = f"{self.base_url}/polyanets"
		data = {"candidateId": self.candidate_id ,"row": row, "column": column}
		self._post(url, data)

	def create_soloon(self, row, column, color):
		"""Creates a SOLOON with the given color at the specified row and column

		Args:
			row (int): The row position
			column (int): The column position
			color (str): The color of the SOLOON
		"""
		url = f"{self.base_url}/soloons"
		data = {"candidateId": self.candidate_id ,"row": row, "column": column, "color":color}
		self._post(url, data)

	def create_cometh(self, row, column, direction):
		"""Creates a COMETH facing the given direction at the specified row and column

		Args:
			row (int): The row position
			column (int): The column position
			direction (str): The direction of the COMETH
		"""
		url = f"{self.base_url}/comeths"
		data = {"candidateId": self.candidate_id ,"row": row, "column": column, "direction":direction}
		self._post(url, data)

	def get_goal_map(self):
		"""Retrieves the current goal map of the candidate

		Returns:
			dict: The retrieved goal map
		"""
		url = f"{self.base_url}/map/{self.candidate_id}/goal"
		try:
			response = requests.get(url)
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as err:
			self._handle_error(err)

	def _post(self, url, data):
		"""Helper method for sending POST requests with exponential backoff

		Args:
			url (str): The API URL for the POST request
			data (dict): The data to send in the POST request

		Returns:
			dict: The response from the API
		
		Raises:
			Exception: If the maximum number of retries (5) is reached
			HTTPError: Raised by the _handle_error method when an HTTP 
				error other than 429 occurs
			RequestException: Raised by the _handle_error method when a
				general request exception occurs
		"""
		max_retries = 5
		retry_delay = 1
		for attempt in range(max_retries):
			try:
				response = requests.post(url, json=data)
				response.raise_for_status()
				return response.json()
			except requests.exceptions.HTTPError as err:
				if response.status_code == 429:
					print(f"Too Many Requests for url. Waiting {retry_delay} seconds before retrying...")
					time.sleep(retry_delay)
					retry_delay *= 2
				else:
					self._handle_error(err)
					break
			except requests.exceptions.RequestException as err:
				self._handle_error(err)
				break
			
		raise Exception("Maximum retry attempts reached")

	def _handle_error(self, error, re_raise=False):
		"""Handles the API request errors

		Args: 
			error (Exception): The exception raised during the API request
			re_raise (bool): Re-raises the caught exception

		Raises:
			RequestException: Re-raises the caught exception with specific messages if re_raise=True
		"""
		if isinstance(error, requests.exceptions.HTTPError):
			if error.response is not None:
				status_code = error.response.status_code
				if status_code == 404:
					message = f"{status_code} Not found. The URL may be wrong. \n\tCheck the API_URL value in the .env file."
				elif status_code == 429:
					message = f"{status_code} Too Many Requests. Wait before trying again."
				elif status_code == 500:
					message = f"{status_code} Internal Server Error. \n\tCheck the CANDIDATE_ID value in the .env file."
				else:
					message = f"HTTP Error occurred: {status_code}"
			else:
				message= f"HTTP Error occured. No response received."
		elif isinstance(error, requests.exceptions.Timeout):
			message = f"The request timed out. Wait before trying again."
		elif isinstance(error, requests.exceptions.ConnectionError):
			message = f"Connection Error. The URL may be wrong. \n\tCheck the API_URL in the .env file."
		elif isinstance(error, requests.exceptions.MissingSchema):
			message = f"Invalid URL. Make sure to add an URL to API_URL variable in the .env file."
		else:
			message = f"Unexpected error occurred: {error}"
		print(f"API request failed: {message}")
		if re_raise:
			raise error

