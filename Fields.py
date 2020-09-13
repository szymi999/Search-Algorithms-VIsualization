class Field:
	#-------- class responsible for informations about certain field -----------

	def __init__(self, x, y, width, height, start, finish, visited):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.start = start
		self.finish = finish
		self.visited = visited
		self.parent = None
		self.wall = False

	def set_parent(self, parent):
		self.parent = parent

	def get_parent(self):
		return self.parent