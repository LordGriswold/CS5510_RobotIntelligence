
# Credit for this: Nicholas Swift
# as found at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
from warnings import warn
import heapq
import time
from math import dist
from Q7Pathing.Dijkstra.dijkstra import Dijkstra
from Q7Pathing.AStar.a_star import AStarPlanner as OtherAstarPlanner
from Q7Pathing.RRTStar.rrt_star import RRTStar
from Q7Pathing.BidirectionalAStar.bidirectional_a_star import BidirectionalAStarPlanner

class Node:
	"""
	A node class for A* Pathfinding
	"""

	def __init__(self, parent=None, position=None):
		self.parent = parent
		self.position = position

		self.g = 0
		self.h = 0
		self.f = 0

	def __eq__(self, other):
		return self.position == other.position
	
	def __repr__(self):
		return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"
	
	# defining less than for purposes of heap queue
	def __lt__(self, other):
		return self.f < other.f
	
	# defining greater than for purposes of heap queue
	def __gt__(self, other):
		return self.f > other.f

def return_path(current_node):
	path = []
	current = current_node
	while current is not None:
		path.append(current.position)
		current = current.parent
	return path[::-1]  # Return reversed path


def astar(maze, start, end, allow_diagonal_movement = True):
	"""
	Returns a list of tuples as a path from the given start to the given end in the given maze
	:param maze:
	:param start:
	:param end:
	:return:
	"""

	# Create start and end node
	start_node = Node(None, start)
	start_node.g = start_node.h = start_node.f = 0
	end_node = Node(None, end)
	end_node.g = end_node.h = end_node.f = 0

	# Initialize both open and closed list
	open_list = []
	closed_list = []

	# Heapify the open_list and Add the start node
	heapq.heapify(open_list) 
	heapq.heappush(open_list, start_node)

	# Adding a stop condition
	outer_iterations = 0
	max_iterations = (len(maze[0]) * len(maze) * 2)

	# what squares do we search
	adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
	if allow_diagonal_movement:
		adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

	# Loop until you find the end
	while len(open_list) > 0:
		outer_iterations += 1

		if outer_iterations > max_iterations:
			# if we hit this point return the path such as it is
			# it will not contain the destination
			warn("giving up on pathfinding too many iterations")
			return return_path(current_node)       
		
		# Get the current node
		current_node = heapq.heappop(open_list)
		closed_list.append(current_node)

		# Found the goal
		if current_node == end_node:
			return return_path(current_node)

		# Generate children
		children = []
		
		for new_position in adjacent_squares: # Adjacent squares

			# Get node position
			node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

			# Make sure within range
			if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
				continue

			# Make sure walkable terrain
			if maze[node_position[0]][node_position[1]] != 0:
				continue

			# Create new node
			new_node = Node(current_node, node_position)

			# Append
			children.append(new_node)

		# Loop through children
		for child in children:
			# Child is on the closed list
			if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
				continue

			# Create the f, g, and h values
			child.g = current_node.g + 1
			child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
			child.f = child.g + child.h

			# Child is already in the open list
			if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
				continue

			# Add the child to the open list
			heapq.heappush(open_list, child)

	warn("Couldn't get a path to destination")
	return None


def GetCostForAlgo(path):
	pathDist = 0
	for i in range(len(path)-1):
		pathDist += dist(path[i], path[i+1])
	return pathDist

def ProblemA():
	maze = []
	# Construct maze
	for y in range(46):
		line = []
		for x in range(46):
			if x == 15 and y <= 25:
				line.append(1)
			if x == 25 and y >= 15:
				line.append(1)
			else:
				line.append(0)
		maze.append(line)
	startPoint = (10,10)
	goalPoint = (30,30)

	# Construct RRT_Star obstacles
	rrtObstacles = []
	for y in range(-5, 36):
		for x in range(-5, 36):
			if x == -5 or y == -5 or y == 35 or x == 35:
				rrtObstacles.append((x, y, 1))
			if x == 10 and y <= 20:
				rrtObstacles.append((x, y, 1))
			if x == 20 and y >= 10:
				rrtObstacles.append((x, y, 1))

	# start and goal position
	sx = 0.0  # [m]
	sy = 0.0  # [m]
	gx = 28.0  # [m]
	gy = 28.0  # [m]
	grid_size = 1.0  # [m]
	robot_radius = 0.5  # [m]

	# set obstacle positions
	ox, oy = [], []
	for i in range(-5, 30):
		ox.append(i)
		oy.append(-5.0)
	for i in range(-5, 30):
		ox.append(30.0)
		oy.append(i)
	for i in range(-5, 31):
		ox.append(i)
		oy.append(30.0)
	for i in range(-5, 31):
		ox.append(-5.0)
		oy.append(i)
	for i in range(-5, 20):
		ox.append(10.0)
		oy.append(i)
	for i in range(0, 20):
		ox.append(20.0)
		oy.append(30.0 - i)

	# Initialize lists for each Algo
	dijkstraHistory = []
	dijkstraTime = 0
	biDirectionalAStarHistory = []
	biDirectionalTime = 0
	rrtStarHistory = []
	rrtStarTime = 0
	aStarHistory = []
	aStarTime = 0
	otherAstarHistory = []
	otherAstarTime = 0

	# Plan each algo
	print("Calculating paths for each Algorithm...")
	for i in range(1, 11):
		dijkstra = Dijkstra(ox, oy, grid_size, robot_radius)
		biDirectionalAStar = BidirectionalAStarPlanner(ox, oy, grid_size, robot_radius)
		a_star = OtherAstarPlanner(ox, oy, grid_size, robot_radius)
		rrt_star = RRTStar(start=[sx, sy], goal=[gx, gy], rand_area=[0, 30], obstacle_list=rrtObstacles, expand_dis=15)

		startTime = time.time()
		brx, bry = biDirectionalAStar.planning(sx=sx, sy=sy, gx=gx, gy=gy)
		biDirectionalTime += (time.time() - startTime)
		biDirectionalAStarPath = list(zip(brx, bry))

		startTime = time.time()
		oarx, oary = a_star.planning(sx=sx, sy=sy, gx=gx, gy=gy)
		otherAstarTime += (time.time() - startTime)
		otherAstarPath = list(zip(oarx, oary))

		startTime = time.time()
		rrtStarPath = rrt_star.planning(False)
		rrtStarTime += (time.time() - startTime)

		startTime = time.time()
		aStarPath = astar(maze, startPoint, goalPoint)
		aStarTime += (time.time() - startTime)

		startTime = time.time()
		drx, dry = dijkstra.planning(sx=sx, sy=sy, gx=gx, gy=gy)
		dijkstraTime += (time.time() - startTime)
		dijkstraPath = list(zip(drx, dry))

		# Get the cost for each run
		dijkstraHistory.append(GetCostForAlgo(dijkstraPath))
		biDirectionalAStarHistory.append(GetCostForAlgo(biDirectionalAStarPath))
		rrtStarHistory.append(GetCostForAlgo(rrtStarPath))
		otherAstarHistory.append(GetCostForAlgo(otherAstarPath))
		aStarHistory.append(GetCostForAlgo(aStarPath))

		print(f"{i}/10 rounds complete.")

	# Get the Average time for each algo
	dijkstraAverageTime = dijkstraTime/10
	biDirectionalAverageTime = biDirectionalTime/10
	rrtStarAverageTime = rrtStarTime/10
	otherAstarAverageTime = otherAstarTime/10
	aStarAverageTime = aStarTime/10

	dijkstraAverageCost = sum(dijkstraHistory)/len(dijkstraHistory)
	biDirectionalAverageCost = sum(biDirectionalAStarHistory)/len(biDirectionalAStarHistory)
	rrtStarAverageCost = sum(rrtStarHistory)/len(rrtStarHistory)
	otherAstarAverageCost = sum(otherAstarHistory)/len(otherAstarHistory)
	aStarAverageCost = sum(aStarHistory)/len(aStarHistory)

	print("===============================================================")
	print("Times")
	print(f"Dijkstra Average Time: {dijkstraAverageTime}")
	print(f"Bi Directional Average Time: {biDirectionalAverageTime}")
	print(f"RRT-Star Average Time: {rrtStarAverageTime}")
	print(f"Other A* Average Time: {otherAstarAverageTime}")
	print(f"Implemented A* Average Time: {aStarAverageTime}")
	print("===============================================================")
	print("Costs")
	print(f"Dijsktra Average Cost: {dijkstraAverageCost}")
	print(f"Bi Directional Average Cost: {biDirectionalAverageCost}")
	print(f"RRT-Star Average Cost: {rrtStarAverageCost}")
	print(f"Other A* Average Cost: {otherAstarAverageCost}")
	print(f"Implemented A* Average Cost: {aStarAverageCost}")
	print("===============================================================")
	print("1. The lowest cost on average was the Implemented A* Algorithm.")
	print("2. The fastest planner on average was the Implemented A* Algorithm.")
	print("3. I noticed that in the starter code, the implemented planner was not able to traverse diagonally. After turning on that feature, it became much faster and more cost effective.")
	print("4. The implemented A* Algorithm appears to be the best one overall so long as we allow it to move diagonally. I would use this planner in a complex environment because of its ability to travel towards the goal without needing to scan every possible node in a given environment. It does this cheap and quickly compared to the other algorithms.")
	print("===============================================================")

def main():
	ProblemA()

if __name__ == "__main__":
	main()