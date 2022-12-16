from math import sin, cos, pi
from matplotlib import pyplot as plt

class SkidSteerRobot:
	
	# width - The width of the robot
	# commands - Commands to run (if empty, commands can be generated later)
	# startX - The starting x position
	# startY - The starting y position
	# startTheta - The starting heading of the robot
	# dt - the time interval that commands will be executed in
	# name - Name of the robot (for plotting purposes)
	def __init__(self, width, commands=[], startX=0, startY=0, startTheta=0, dt=0.1, name="Skid Steer Robot"):
		self.__name = name
		self.__width = width
		
		self.__xPositions = [startX]
		self.__yPositions = [startY]
		self.__thetas = [startTheta]
		
		self.__deltaX = [0]
		self.__deltaY = [0]
		self.__deltaTheta = [0]
		
		self.__commandsToRun = commands
		self.__commandsRun = [] # List of commands that have been run
		self.__dt = dt
	
	# Takes the previous position of robot, and calculates where it will end up
	# given certain wheel velocities and time to travel.
	# vLeft - Left Wheel Velocity
	# vRight - Right Wheel Velocity
	# x - Current x position
	# y - Current y position
	# theta - Current angle position
	# Returns the new x, y, and theta postions.
	def move(self, vRight, vLeft, x, y, theta):
		dx = -1*((vLeft + vRight)/2.0)*(sin(theta))*self.__dt
		newX = x + dx
		dy = ((vLeft + vRight)/2.0)*(cos(theta))*self.__dt
		newY = y + dy
		dTheta = ((vLeft - vRight)/self.__width)*self.__dt
		newTheta = theta + dTheta
		
		self.__deltaX.append(round(dx, 3))
		self.__deltaY.append(round(dy, 3))
		self.__deltaTheta.append(round(dTheta, 3))
		
		return newX, newY, newTheta
	
	# Add a command to the list of commands
	# lv - Left wheel velocity (meters per second)
	# rv - Right wheel velocity (meters per second)
	# t - duration (seconds)
	def addCommand(self, lv, rv, t):
		self.__commandsToRun.append((lv, rv, t))
		
	# Adds a command to move forward, given a velocity and distance
	def forward(self, v, d):
		t = d / v
		self.__commandsToRun.append((v, v, t))
	
	# Generates a command that turns the robot in place at an angle theta radians.
	# Use a positive theta for a left turn, and a negative theta for a right turn
	# v - The magnitude of the velocity of the left and right sides (meters per second)
	# theta - the turning angle (radians)
	def turn(self, v, theta):
		if theta > 0: # left turn
			vRight = v
			vLeft = -v
		else: # right turn
			vRight = -v
			vLeft = v
		t = abs(theta / ((2 * v) / self.__width))
		self.__commandsToRun.append((vLeft, vRight, t))
	
	# Generates a command that moves the robot along the path of an arc
	# v - The velocity to move along the arc
	# r - the radius of curvature of the arc
	# d - the distance to move along the arc
	def arc(self, v, r, d):
		theta = v / r
		rv = v + ((theta * self.__width) / 2)
		lv = v - ((theta * self.__width) / 2)
		t = d / v
		self.__commandsToRun.append((lv, rv, t))
	
	# Generates a command that moves the robot in a complete circle
	# v - the speed to move around the circle
	# r - the radius of the circle
	def circle(self, v, r):
		self.arc(v, r, 2*pi*r)
		
	# Given a list of commands it will plot the path of
	# a Skid Steer robot.
	# dt - Time to execute command.
	# Returns void
	def runCommands(self):
		for command in self.__commandsToRun:
			# Initialize variables for robot
			timeElapsed = 0
			goalTime = command[2]
			Lv = command[0]
			Rv = command[1]
			x = self.__xPositions[len(self.__xPositions) - 1]
			y = self.__yPositions[len(self.__yPositions) - 1]
			theta = self.__thetas[len(self.__thetas) - 1]

			# Move robot until goal time is reached
			numiters = 0
			while timeElapsed < goalTime:
				x, y, theta = self.move(Lv, Rv, x, y, theta)

				self.__xPositions.append(round(x, 3))
				self.__yPositions.append(round(y, 3))
				self.__thetas.append(round(theta, 3))

				timeElapsed += self.__dt
				timeElapsed = round(timeElapsed, 1)
				numiters += 1
			self.__commandsRun.append(command)
		self.__commandsToRun.clear()
	
	# Plot the course the robot has travelled
	def plotCourse(self):
		plt.plot(self.__xPositions, self.__yPositions)
		plt.xlabel(f"X - Axis in Meters")
		plt.ylabel(f"Y - Axis in Meters")
		plt.title(self.__name)
		plt.show()

	# Plots all the graphs needed for midterm 1a question.
	def plotEverything(self):
		plt.plot(self.__xPositions, self.__yPositions)
		plt.xlabel("X - Axis in Meters")
		plt.ylabel("Y - Axis in Meters")
		plt.title("Midterm 1a")
		plt.show()

		plt.plot(self.__thetas)
		plt.xlabel("Command Number")
		plt.ylabel("Radian Position")
		plt.title("Midterm 1a - Trajectory")
		plt.show()

		plt.plot(self.__deltaX)
		plt.xlabel("Command Number")
		plt.ylabel("Change in X")
		plt.title("Midterm 1a - Change in X vs Command Number")
		plt.show()

		plt.plot(self.__deltaY)
		plt.xlabel("Command Number")
		plt.ylabel("Change in Y")
		plt.title("Midterm 1a - Change in Y vs Command Number")
		plt.show()

		plt.plot(self.__deltaTheta)
		plt.xlabel("Command Number")
		plt.ylabel("Change in Theta")
		plt.title("Midterm 1a - Change in Theta vs Command Number")
		plt.show()
	
	# returns all commands that have already been run
	def getCommandsRun(self):
		return self.__commandsRun
	
	# returns all commands that have not yet been run
	def getCommandsToRun(self):
		return self.__commandsToRun

	def printCommandsRun(self):
		print(f"Commands run by {self.__name}:")
		for command in self.__commandsRun:
			print(f"\t{command}")
		
if __name__ == '__main__':
	bot = SkidSteerRobot(0.55)
	# bot.forward(8.0, 2.5)
	# bot.turn(8.0, pi/2)
	bot.arc(8.0, 1.25, pi * 1.25)
	bot.circle(8.0, 2.5)
	bot.runCommands()
	bot.plotCourse()
	bot.printCommandsRun()
	