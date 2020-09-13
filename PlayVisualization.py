import time
import math

class PlayVisualization:
	#----------- class responsible for visualization ---------------

	def __init__(self, windowWidth, windowHeight, fieldWidth, fieldHeight, start=None, finish=None, fields=None, simulation=False):
		#---------- define some basic variables -----------
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.fieldWidth = fieldWidth
		self.fieldHeight = fieldHeight

		self.algorithm = 0	# which algorithm 0-BFS, 1-DFS, 2-A*, 3-Dijkstra
		self.start = start 	# start node
		self.finish = finish 	# finish node
		self.fields = fields 	# list with informations about every field on map
		self.simulation = simulation # 1 if visualization is runing otherwise 0

	def play(self, canvas):
		# method defining which algorithm will be used

		if self.algorithm == 0:
			self.breadth_first_search(canvas)
		elif self.algorithm == 1:
			self.depth_first_search(canvas)
		elif self.algorithm == 2:
			self.search_aStar(canvas)
		else:
			self.search_dijkstra(canvas)

	def set_algorithm(self, a):
		# setting which algorithm 

		self.algorithm = a

	def set_fields(self, fields):
		# defining start and finish nodes

		self.fields = fields
		for field in fields:
			for f in field:
				if f.start:
					self.start = f
				if f.finish:
					self.finish = f

	def breadth_first_search(self, canvas):
		# BFS algorithm 

		queue = []
		queue.append(self.start)
		while self.simulation:
			if queue[0] == self.finish:
				# finish node is found
				
				print("KONIEC")
				self.draw_shortest_path(canvas)
				break
			elif not queue:
				# path not found

				print("Nie udało się znaleźć drogi")
				break

			neighbours = self.check_neighbours(queue[0], queue, canvas)

	def depth_first_search(self, canvas):
		# DFS algorithm

		queue = []
		queue.append(self.start)
		neighbours = []
		neighbours.append(queue[0])
		while self.simulation:
			if self.finish in neighbours:
				# finish node found

				print("KONIEC")
				self.draw_shortest_path(canvas)
				break
			elif not queue:
				# path not found
				print("Nie udało się znaleźć drogi")
				break

			if neighbours:
				neighbours = self.check_neighbours(neighbours[0], queue, canvas)
			else:
				# when there isnt any neighbour free check last node added to queue
				neighbours = self.check_neighbours(queue[-1], queue, canvas)

	def check_neighbours(self, node, queue, canvas):
		# method where is checking for neighbours in BFS and DFS algorithm

		vertical = [-1, 0, 1, 0]
		horizontal = [0, 1, 0, -1]
		neighbours = []
		node.visited = True
		neighbours_to_delete = []

		# looking for neighbours

		for i in range(4):
			if int(node.y / self.fieldHeight + vertical[i]) > 0 and int(node.y / self.fieldHeight + vertical[i]) < int(0.75 * self.windowHeight / self.fieldHeight) - 1 and int(node.x / self.fieldWidth + horizontal[i]) > 0 and int(node.x / self.fieldWidth + horizontal[i]) < int(self.windowWidth / self.fieldWidth) - 1:
				neighbours.append(self.fields[int(node.y / self.fieldHeight + vertical[i])][int(node.x / self.fieldWidth + horizontal[i])])

		# which neighbours arent available, delete them

		for n in neighbours:
			if n in queue:
				neighbours_to_delete.append(n)
			elif n.visited:
				neighbours_to_delete.append(n)
			elif n.wall:
				neighbours_to_delete.append(n)

		for d in neighbours_to_delete:
			neighbours.remove(d)

		for n in neighbours:
			# set parents to be able to search for shortest path
			n.set_parent(node)
			self.draw_neighbours(n.x, n.y, n.width, n.height, canvas)
			queue.append(n)

		self.draw_visited(node.x, node.y, node.width, node.height, canvas)
		if node in queue:
			queue.remove(node)

		return neighbours

	def search_dijkstra(self, canvas):
		# Dijkstra algorithm

		nodes = []
		nodes.append({"node": self.start, "distance": 0})
		completedNodes = []
		current = nodes[0]
		while self.simulation:
			if not nodes:
				print("Nie udało się znaleźć drogi")
				break

			if current["node"] == self.finish:
				print("KONIEC")
				self.draw_shortest_path(canvas)
				break

			self.check_neighbours_dijkstra(current, nodes, completedNodes, canvas)

			# looking for node with the least distance from start

			indexOfMinValue = 0
			for i, n in enumerate(nodes):
				if n["distance"] < nodes[indexOfMinValue]["distance"]:
					indexOfMinValue = i

			current = nodes[indexOfMinValue]

	def check_neighbours_dijkstra(self, node, nodes, completedNodes, canvas):
		xx = [0, 1, 1, 1, 0, -1, -1, -1]
		yy = [-1, -1, 0, 1, 1, 1, 0, -1]
		neighbours = []
		node["node"].visited = True
		neighbours_to_delete = []

		# looking for neighbours
		for i in range(8):
			if (
					int(node["node"].y / self.fieldHeight + yy[i]) > 0 and 
					int(node["node"].y / self.fieldHeight + yy[i]) < int(0.75 * self.windowHeight / self.fieldHeight) - 1 and 
					int(node["node"].x / self.fieldWidth + xx[i]) > 0 and 
					int(node["node"].x / self.fieldWidth + xx[i]) < int(self.windowWidth / self.fieldWidth) - 1
				):
				if i % 2 == 0:
					neighbours.append({"node":self.fields[int(node["node"].y / self.fieldHeight + yy[i])][int(node["node"].x / self.fieldWidth + xx[i])], 
										"distance": node["distance"] + 10})
				else:
					neighbours.append({"node":self.fields[int(node["node"].y / self.fieldHeight + yy[i])][int(node["node"].x / self.fieldWidth + xx[i])], 
										"distance": node["distance"] + 14})		

		# which neighbours arent available, delete them
		for neighbour in neighbours:
			for n in nodes:
				if neighbour["node"] == n["node"] and neighbour["distance"] >= n["distance"]:
					neighbours_to_delete.append(neighbour)
					break
			for c in completedNodes:
				if neighbour["node"] == c["node"]:
					neighbours_to_delete.append(neighbour)
					break
			if neighbour["node"].wall:
				neighbours_to_delete.append(neighbour)

		for d in neighbours_to_delete:
			neighbours.remove(d)

		for n in neighbours:
			# if the better node was found(with shortest distance), replace previous(worse)
			for neighbour in nodes:
				if n["node"] == neighbour["node"]:
					nodes.remove(neighbour)
			# add parents to find shortest path
			n["node"].parent = node["node"]
			nodes.append(n)
			self.draw_neighbours(n["node"].x, n["node"].y, n["node"].width, n["node"].height, canvas)

		completedNodes.append(node)
		self.draw_visited(node["node"].x, node["node"].y, node["node"].width, node["node"].height, canvas)
		nodes.remove(node)

	def search_aStar(self, canvas):
		# A* algorithm

		nodes = []
		h = self.h_cost(self.start)
		nodes.append({"node": self.start, "g": 0, "h": h})
		completedNodes = []
		current = nodes[0]
		while self.simulation:
			if not nodes:
				print("Nie udało się znaleźć drogi")
				break

			if current["node"] == self.finish:
				print("KONIEC")
				self.draw_shortest_path(canvas)
				break

			self.check_neighbours_aStar(current, nodes, completedNodes, canvas)

			# looking for node with the least distance from start

			indexOfMinValue = 0
			for i, n in enumerate(nodes):
				if n["h"] + n["g"] < nodes[indexOfMinValue]["h"] + nodes[indexOfMinValue]["g"]:
					indexOfMinValue = i
				elif n["h"] + n["g"] == nodes[indexOfMinValue]["h"] + nodes[indexOfMinValue]["g"]:
					if n["h"] < nodes[indexOfMinValue]["h"]:
						indexOfMinValue = i

			current = nodes[indexOfMinValue]

	def check_neighbours_aStar(self, node, nodes, completedNodes, canvas):
		xx = [0, 1, 1, 1, 0, -1, -1, -1]
		yy = [-1, -1, 0, 1, 1, 1, 0, -1]
		neighbours = []
		node["node"].visited = True
		neighbours_to_delete = []

		# which neighbours arent available, delete them
		for i in range(8):
			if (
					int(node["node"].y / self.fieldHeight + yy[i]) > 0 and 
					int(node["node"].y / self.fieldHeight + yy[i]) < int(0.75 * self.windowHeight / self.fieldHeight) - 1 and 
					int(node["node"].x / self.fieldWidth + xx[i]) > 0 and 
					int(node["node"].x / self.fieldWidth + xx[i]) < int(self.windowWidth / self.fieldWidth) - 1
				):
				if i % 2 == 0:
					neighbours.append({"node":self.fields[int(node["node"].y / self.fieldHeight + yy[i])][int(node["node"].x / self.fieldWidth + xx[i])], 
										"g": node["g"] + 10,
										"h": self.h_cost(self.fields[int(node["node"].y / self.fieldHeight + yy[i])][int(node["node"].x / self.fieldWidth + xx[i])])})
				else:
					neighbours.append({"node":self.fields[int(node["node"].y / self.fieldHeight + yy[i])][int(node["node"].x / self.fieldWidth + xx[i])], 
										"g": node["g"] + 14,
										"h": self.h_cost(self.fields[int(node["node"].y / self.fieldHeight + yy[i])][int(node["node"].x / self.fieldWidth + xx[i])])})		

		for neighbour in neighbours:
			for n in nodes:
				if neighbour["node"] == n["node"] and neighbour["h"] + neighbour["g"] >= n["h"] + n["g"]:
					neighbours_to_delete.append(neighbour)
					break
			for c in completedNodes:
				if neighbour["node"] == c["node"]:
					neighbours_to_delete.append(neighbour)
					break
			if neighbour["node"].wall:
				neighbours_to_delete.append(neighbour)

		for d in neighbours_to_delete:
			neighbours.remove(d)

		for n in neighbours:
			for neighbour in nodes:
				# if the better node was found(with shortest distance), replace previous(worse)
				if n["node"] == neighbour["node"]:
					nodes.remove(neighbour)
			n["node"].parent = node["node"]
			nodes.append(n)
			self.draw_neighbours(n["node"].x, n["node"].y, n["node"].width, n["node"].height, canvas)

		completedNodes.append(node)
		self.draw_visited(node["node"].x, node["node"].y, node["node"].width, node["node"].height, canvas)
		nodes.remove(node)

	def h_cost(self, node):
		# return h cost(distance from start + distance to finish) of field in A* algorithm
		return int(math.sqrt(math.pow(self.finish.x - node.x, 2) + math.pow(self.finish.y - node.y, 2)))

	def draw_visited(self, x, y, width, height, canvas):
		# draw visited nodes on green

		color = "green"

		if self.start.x == x and self.start.y == y or self.finish.x == x and self.finish.y == y:
			color = "red"

		canvas.create_rectangle(x, y, width, height, outline="black", fill=color)
		canvas.update()

	def draw_neighbours(self, x, y, width, height, canvas):
		# draw neighbours on yellow

		color = "yellow"

		if self.start.x == x and self.start.y == y or self.finish.x == x and self.finish.y == y:
			color = "red"

		canvas.create_rectangle(x, y, width, height, outline="black", fill=color)
		canvas.update()

	def draw_shortest_path(self, canvas):
		# find by parents shortest path
		path = []
		node = self.finish.get_parent()
		while node.get_parent() is not None:
			path.append(node)
			node = node.get_parent()

		# draw shortest path on purple
		for p in path:
			canvas.create_rectangle(p.x, p.y, p.width, p.height, outline="black", fill="purple")
			canvas.update()
			time.sleep(0.01)