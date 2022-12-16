from cProfile import label
from matplotlib import pyplot as plt
from math import dist, sin, cos, pi
from MobileRobots import SkidSteer as sks
from MobileRobots import AckermannSteer as aks
# Sizes are in meters
LENGTH = 0.75
WIDTH = 0.55
LEFT_TURN = (-.4319689899, .4319689899, 1)

# Positions after commands
xPositions = [0]
yPositions = [0]
thetaPositions = [0]

# The change in positions after commands
deltaX = [0]
deltaY = [0]
deltaTheta = [0]

# Takes the previous position of robot, and calculates where it will end up
# given certain wheel velocities and time to travel.
# Lv - Left Wheel Velocity
# RV - Right Wheel Velocity
# x - Current x position
# y - Current y position
# theta - Current angle position
# dt - Time to execute command
# Returns the new x, y, and theta postions.
def SkidSteerMovement(Lv, Rv, x, y, theta, dt=0.1):
	dx = -1*((Rv + Lv)/2.0)*(sin(theta))*dt
	newX = x + dx
	dy = ((Rv + Lv)/2.0)*(cos(theta))*dt
	newY = y + dy
	dTheta = ((Rv - Lv)/WIDTH)*dt
	newTheta = theta + dTheta

	deltaX.append(round(dx, 3))
	deltaY.append(round(dy, 3))
	deltaTheta.append(round(dTheta, 3))
	return newX, newY, newTheta

# Given a list of commands it will plot the path of
# a Skid Steer robot.
# listOfCommands - A list of tuples containing command data
# dt - Time to execute command.
# Returns void
def RunCommands(listOfCommands, dt = 0.1):
	for command in listOfCommands:
		# Initialize variables for robot
		timeElapsed = 0
		goalTime = command[2]
		Lv = command[0]
		Rv = command[1]
		x = xPositions[len(xPositions) - 1]
		y = yPositions[len(yPositions) - 1]
		theta = thetaPositions[len(thetaPositions) - 1]

		# Move robot until goal time is reached
		numiters = 0
		while timeElapsed < goalTime:
			x, y, theta = SkidSteerMovement(Lv, Rv, x, y, theta, dt)

			xPositions.append(round(x, 3))
			yPositions.append(round(y, 3))
			thetaPositions.append(round(theta, 3))

			timeElapsed += dt
			timeElapsed = round(timeElapsed, 1)
			numiters += 1

# Resets the position lists so that we can reuse them on another problem.
# Returns void
def ResetPositions():
	xPositions.clear()
	yPositions.clear()
	thetaPositions.clear()
	xPositions.append(0)
	thetaPositions.append(0)
	yPositions.append(0)

	deltaX.clear()
	deltaY.clear()
	deltaTheta.clear()
	deltaX.append(0)
	deltaY.append(0)
	deltaTheta.append(0)

def FindError(realX, realY, robotX, robotY):
	positionError = []
	for i in range(len(realX)-1):
		positionError.append(dist([realX[i], realY[i]], [robotX[i], robotY[i]]))

	return positionError


def ProblemA():
	bot = sks.SkidSteerRobot(0.55)
	bot.addCommand(6.05, 9.95, .4)
	bot.addCommand(7.05, 8.95, 1.9)
	bot.runCommands()

	bot.plotEverything()
	print("----------Skid Steer Commands to Trace a 5m Circle----------")
	bot.printCommandsRun()

def ProblemB():
	bot = aks.AckermannSteerRobot(0.75)
	bot.addCommand(0.55, 8, 1.4)
	bot.addCommand(0.3, 8, 2)
	bot.runCommands()

	bot.plotEverything()
	print("----------Akermann Steer Commands to Trace a 5m Circle----------")
	bot.printCommandsRun()

def ProblemC():
	# For dt = 1
	bot = aks.AckermannSteerRobot(0.75, dt=1)
	bot.addCommand(0.29145, 8, 10)
	bot.runCommands()

	realX, realY = bot.findRealPositionsOnCircle((0.29145, 8, 10), 2.5)

	dt1positionError = FindError(realX, realY, bot.getXPositions(), bot.getYPositions())
	plt.plot(dt1positionError, label = "dt=1")
	plt.axis([0, 10, 0, 10])
	plt.title("Midterm 1c - Error Over Time")
	plt.xlabel("Time in Seconds")
	plt.ylabel("Error")
	plt.legend()
	plt.show()

	# For dt = 0.1
	bot = aks.AckermannSteerRobot(0.75, dt=0.1)
	bot.addCommand(0.29145, 8, 10)
	bot.runCommands()

	realX, realY = bot.findRealPositionsOnCircle((0.29145, 8, 10), 2.5)

	dt2positionError = FindError(realX, realY, bot.getXPositions(), bot.getYPositions())
	plt.plot(dt2positionError, label = "dt=0.1")
	plt.axis([0, 100, 0, 10])
	plt.title("Midterm 1c - Error Over Time")
	plt.xlabel("Time in Deciseconds")
	plt.ylabel("Error")
	plt.legend()
	plt.show()

	# For dt = 0.01
	bot = aks.AckermannSteerRobot(0.75, dt=0.01)
	bot.addCommand(0.29145, 8, 10)
	bot.runCommands()

	realX, realY = bot.findRealPositionsOnCircle((0.29145, 8, 10), 2.5)

	dt3positionError = FindError(realX, realY, bot.getXPositions(), bot.getYPositions())
	plt.plot(dt3positionError, label = "dt=0.01")
	plt.axis([0, 1000, 0, 10])
	plt.title("Midterm 1c - Error Over Time")
	plt.xlabel("Time in Centiseconds")
	plt.ylabel("Error")
	plt.legend()
	plt.show()

	dts = ["dt=1", "dt=0.1", "dt=0.01"]
	results = [len(dt1positionError), len(dt2positionError), len(dt3positionError)]
	plt.bar(dts, results)
	plt.title("Midterm 1c - Approximate Computations")
	plt.ylabel("Number of Computations")
	plt.show()


def main():
	ProblemA()
	ProblemB()
	ProblemC()

if __name__ == "__main__":
	main()