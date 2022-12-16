from math import sin, cos, tan, atan, pi
from matplotlib import pyplot as plt

class AckermannSteerRobot:
	
	# length - The length of the robot (meters)
	# commands - Commands to run (if empty, commands can be generated later)
	# startX - The starting x position
	# startY - The starting y position
	# startTheta - The starting heading of the robot
	# dt - the time interval that commands will be executed in
	# name - Name of the robot (for plotting purposes)
	def __init__(self, length, commands=[], startX=0, startY=0, startTheta=0, dt=0.1, name="Ackermann Steering Robot"):
		self.__length = length
		self.__name = name
		
		self.__xPositions = [startX]
		self.__yPositions = [startY]
		self.__thetas = [startTheta]
		
		self.__deltaX = [0]
		self.__deltaY = [0]
		self.__deltaTheta = [0]
		
		self.__commandsToRun = commands
		self.__commandsRun = [] # List of commands that have been run
		self.__dt = dt
		
	# v - Velocity of the rear wheels
	# x - position of the robot on the x-axis before the move
	# y - position of the robot on the y-axis before the move
	# theta - angle of the robot relative to the y-axis before the move
	# alpha - steering angle
	# returns the new x, y, and theta positions after the move
	def move(self, v, x, y, theta, alpha):
		dx = -self.__dt * v * sin(theta)
		dy = self.__dt * v * cos(theta)
		dTheta = self.__dt * (v / self.__length) * tan(alpha)
		
		self.__deltaX.append(round(dx, 3))
		self.__deltaY.append(round(dy, 3))
		self.__deltaTheta.append(round(dTheta, 3))
		
		return x + dx, y + dy, theta + dTheta
	
	# Add a command to the list of commands
	# alpha - heading for the front wheels (radians)
	# v - velocity of the back wheels
	# t - duration (seconds)
	def addCommand(self, alpha, v, t):
		self.__commandsToRun.append((alpha, v, t))
		
	# Adds a command to move forward, given a velocity and distance
	def forward(self, v, d):
		t = d / v
		self.__commandsToRun.append((0.0, v, t))
	
	# Generates a command that moves the robot along the path of an arc
	# v - The velocity to move along the arc
	# r - the radius of curvature of the arc
	# d - the distance to move along the arc
	def arc(self, r, v, d):
		alpha = atan(self.__length / r)
		t = d / v
		self.__commandsToRun.append((alpha, v, t))
  
	def circle(self, r, v):
		self.arc(r, v, 2 * pi * r)
		
	# Given a list of commands it will move the ackermann robot.
	def runCommands(self):
		for command in self.__commandsToRun:
			# Initialize variables for robot
			timeElapsed = 0
			goalTime = command[2]
			alpha = command[0]
			v = command[1]
			x = self.__xPositions[len(self.__xPositions) - 1]
			y = self.__yPositions[len(self.__yPositions) - 1]
			theta = self.__thetas[len(self.__thetas) - 1]

			# Move robot until goal time is reached
			numiters = 0
			while timeElapsed < goalTime:
				x, y, theta = self.move(v, x, y, theta, alpha)

				self.__xPositions.append(round(x, 3))
				self.__yPositions.append(round(y, 3))
				self.__thetas.append(round(theta, 3))

				timeElapsed += self.__dt
				timeElapsed = round(timeElapsed, 3)
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
	
	# Plots all the graphs needed for Midterm 1b question
	def plotEverything(self):
		plt.plot(self.__xPositions, self.__yPositions)
		plt.xlabel("X - Axis in Meters")
		plt.ylabel("Y - Axis in Meters")
		plt.title("Midterm 1b")
		plt.show()

		plt.plot(self.__thetas)
		plt.xlabel("Command Number")
		plt.ylabel("Radian Position")
		plt.title("Midterm 1b - Trajectory")
		plt.show()

		plt.plot(self.__deltaX)
		plt.xlabel("Command Number")
		plt.ylabel("Change in X")
		plt.title("Midterm 1b - Change in X vs Command Number")
		plt.show()

		plt.plot(self.__deltaY)
		plt.xlabel("Command Number")
		plt.ylabel("Change in Y")
		plt.title("Midterm 1b - Change in Y vs Command Number")
		plt.show()

		plt.plot(self.__deltaTheta)
		plt.xlabel("Command Number")
		plt.ylabel("Change in Theta")
		plt.title("Midterm 1b - Change in Theta vs Command Number")
		plt.show()
	
	# returns all commands that have already been run
	def getCommandsRun(self):
		return self.__commandsRun
	
	# returns all commands that have not yet been run
	def getCommandsToRun(self):
		return self.__commandsToRun
	
	def getXPositions(self):
		return self.__xPositions

	def getYPositions(self):
		return self.__yPositions

	def printCommandsRun(self):
		print(f"Commands run by {self.__name}:")
		for command in self.__commandsRun:
			print(f"\t{command}")

	def findRealPositionsOnCircle(self, command, r):
		realXPositions = [0]
		realYPositions = [0]
		v = command[1]
		dt = self.__dt
		distancePerDt = v*dt
		currentTheta = 0
		for i in range(len(self.__xPositions)):
			realTheta = (distancePerDt/r) + currentTheta
			realXPositions.append((cos(realTheta)*r) - 2.5)
			realYPositions.append(sin(realTheta)*r) 
			currentTheta = realTheta
		return realXPositions, realYPositions


	def findError(self):
		for i in range(len(self.__xPositions)):
			x = self.__xPositions[i]
			y = self.__yPositions[i]
			theta = self.__thetas[i]
		
if __name__ == '__main__':
	bot = AckermannSteerRobot(0.75)
	# bot.addCommand(0.55, 8, 1.4)
	# bot.addCommand(0.3, 8, 2)
	bot.arc(1.25, 8.0, pi * 1.25) # Do a semicircle with 1.25 meter radius
	bot.circle(2.5, 8.0) # Do a circle with 2.5 meter radius
	bot.runCommands()
	bot.plotCourse()
	print("X")
	print(max(bot.getXPositions()))
	print(min(bot.getXPositions()))
	print("Y")
	print(max(bot.getYPositions()))
	print(min(bot.getYPositions()))
	bot.printCommandsRun()
	