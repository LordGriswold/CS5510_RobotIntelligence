from matplotlib import pyplot as plt
from math import sin, cos, pi

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

def ProblemA():

	commandList = [(6.05, 9.95, .4), 
	(7.05, 8.95, 1.9)]
	RunCommands(commandList)
	plt.plot(xPositions, yPositions)
	plt.xlabel("X - Axis in Meters")
	plt.ylabel("Y - Axis in Meters")
	plt.title("Midterm 1a")
	plt.show()

	plt.plot(thetaPositions)
	plt.xlabel("Command Number")
	plt.ylabel("Radian Position")
	plt.title("Midterm 1a - Trajectory")
	plt.show()

	plt.plot(deltaX)
	plt.xlabel("Command Number")
	plt.ylabel("Change in X")
	plt.title("Midterm 1a - Change in X vs Command Number")
	plt.show()

	plt.plot(deltaY)
	plt.xlabel("Command Number")
	plt.ylabel("Change in Y")
	plt.title("Midterm 1a - Change in Y vs Command Number")
	plt.show()

	plt.plot(deltaTheta)
	plt.xlabel("Command Number")
	plt.ylabel("Change in Theta")
	plt.title("Midterm 1a - Change in Theta vs Command Number")
	plt.show()
	print("----------Skid Steer Commands to Trace a 5m Circle----------")
	for command in commandList:
		print(command)
	ResetPositions()

def main():
	ProblemA()

if __name__ == "__main__":
	main()