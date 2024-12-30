class AstralObject:
	"""Superclass for all astral objects"""

	def __init__(self, row, column):
		"""Initializes an AstralObject

		Args:
			row (int): The row position
			column (int): The column position
		"""
		self.row = row
		self.column = column
	
	def create(self, api_client):
		"""Method for creating the astral object using the specified API Client

		Args:
			api_client(ApiClient): The client to interact with the API
		
		Raises:
			NotImplementedError: If the method is not implemented by a subclass
		"""
		raise NotImplementedError("Subclass must implement create method!")

class Polyanet(AstralObject):
	"""Subclass of AstralObject that represents a Polyanet"""

	def create(self, api_client):
		"""Creates a Polyanet using the specified API Client

		Args:
			api_client(ApiClient): The client to interact with the API
		"""
		api_client.create_polyanet(self.row, self.column)

class Soloon(AstralObject):
	"""Subclass of AstralObject that represents a Soloon"""

	def __init__(self, row, column, color):
		"""Initializes a Soloon, inheriting from AstralObject
		
		Args:
			row (int): The row position
			column (int): The column position
			color (str): The color of the Soloon
		"""
		super().__init__(row, column)
		self.color = color

	def create(self, api_client):
		"""Creates a Soloon using the specified API Client

		Args:
			api_client(ApiClient): The client to interact with the API
		"""
		api_client.create_soloon(self.row, self.column, self.color)

class Cometh(AstralObject):
	"""Subclass of AstralObject that represents a Cometh"""

	def __init__(self, row, column, direction):
		"""Initializes a Cometh, inheriting from AstralObject
		
		Args:
			row (int): The row position
			column (int): The column position
			direction (str): The direction of the Cometh
		"""
		super().__init__(row, column)
		self.direction = direction

	def create(self, api_client):
		"""Creates a Cometh using the specified API Client

		Args:
			api_client(ApiClient): The client to interact with the API
		"""
		api_client.create_cometh(self.row, self.column, self.direction)