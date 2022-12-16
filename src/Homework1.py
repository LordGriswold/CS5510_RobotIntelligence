from matplotlib import pyplot as plt
from math import sin, cos
from MobileRobots import SkidSteer

# Sizes are in meters
LENGTH = 0.5
WIDTH = 0.3
LEFT_TURN = (-0.0785398163, 0.0785398163, 3)

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

# Takes the changes in X and Y velocity, the duration of command, and
# records the new position of the Swedish Wheel setup.
# Xv - Velocity in X direction
# Yv - Velocity in Y direction
# goalTime - The total command time
# dt - Time to execute command
def SwedishWheelMovement(Xv, Yv, goalTime, dt=0.1):
	timeElapsed = 0
	x = xPositions[len(xPositions) - 1]
	y = yPositions[len(yPositions) - 1]
	theta = 0

	while timeElapsed < goalTime:
		x += Xv * dt
		y += Yv * dt
		xPositions.append(round(x, 3))
		yPositions.append(round(y, 3))
		thetaPositions.append(round(theta, 3))

		deltaX.append(round(Xv * dt, 3))
		deltaY.append(round(Yv * dt, 3))
		deltaTheta.append(round(theta, 3))
		timeElapsed += dt

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
 
# Returns a command to move forward, given a velocity and time
def forward(v, t):
    return (v, v, t)

# Define Problem Functions Below #

def Problem1():
	#Left Wheel, Right Wheel, Duration
	commandList = [(1.0, 1.5, 5.0), 
					(-1.0, -1.5, 3.0), 
					(0.8, -2.0, 8.0), 
					(2.0, 2.0, 10.0)]
	bot = SkidSteer.SkidSteerRobot(WIDTH, commands=commandList, name="Skid Steer Travel Problem 1")
	bot.runCommands()
	bot.plotCourse()

def Problem2():
	commandList = []
	duration = 4.7
	while(duration > 0):
		duration = round(duration, 1)
		commandList.append((1.0, 1.0, duration))
		commandList.append(LEFT_TURN)
		commandList.append((1.0, 1.0, duration))
		commandList.append(LEFT_TURN)
		if (len(commandList) == 4):
			commandList.append((1.0, 1.0, duration))
			commandList.append(LEFT_TURN)
		duration -= 0.3
	
	RunCommands(commandList)
	plt.plot(xPositions, yPositions)
	plt.xlabel("X - Axis in Meters")
	plt.ylabel("Y - Axis in Meters")
	plt.title("Skid Steer Travel Problem 2")
	plt.show()

	plt.plot(thetaPositions)
	plt.xlabel("Command Number")
	plt.ylabel("Radian Position")
	plt.title("Skid Steer Travel Problem 2 - Trajectory")
	plt.show()

	plt.plot(deltaX)
	plt.xlabel("Command Number")
	plt.ylabel("Change in X")
	plt.title("Skid Steer Travel Problem 2 - Change in X vs Command Number")
	plt.show()

	plt.plot(deltaY)
	plt.xlabel("Command Number")
	plt.ylabel("Change in Y")
	plt.title("Skid Steer Travel Problem 2 - Change in Y vs Command Number")
	plt.show()

	plt.plot(deltaTheta)
	plt.xlabel("Command Number")
	plt.ylabel("Change in Theta")
	plt.title("Skid Steer Travel Problem 2 - Change in Theta vs Command Number")
	plt.show()
	print("----------Skid Steer Commands to Cover 5x5 Square----------")
	for command in commandList:
		print(command)
	ResetPositions()

def Problem3():
	num_cols = round(5/WIDTH)
	commandList = []
	going_up = True

	for i in range(num_cols):
		if going_up:
			# Move up
			Xv = 0
			Yv = 1
			goalTime = 5 - LENGTH
		else:
			# Move down
			Xv = 0
			Yv = -1
			goalTime = 5 - LENGTH
		SwedishWheelMovement(Xv, Yv, goalTime)
		commandList.append((Xv, Yv, goalTime))
		if xPositions[len(xPositions) - 1] < 5 - WIDTH:
			# Move right by WIDTH amount
			Xv = 1
			Yv = 0
			goalTime = WIDTH
			SwedishWheelMovement(Xv, Yv, goalTime)
			commandList.append((Xv, Yv, goalTime))
		going_up = not going_up  # Reverse direction

	plt.plot(xPositions, yPositions)
	plt.xlabel("X - Axis in Meters")
	plt.ylabel("Y - Axis in Meters")
	plt.title("Swedish Wheel Travel Problem 3")
	plt.show()

	plt.plot(thetaPositions)
	plt.xlabel("Command Number")
	plt.ylabel("Radian Position")
	plt.title("Swedish Wheel Travel Problem 3 - Trajectory")
	plt.show()

	plt.plot(deltaX)
	plt.xlabel("Command Number")
	plt.ylabel("Change in X")
	plt.title("Swedish Wheel Travel Problem 3 - Change in X vs Command Number")
	plt.show()

	plt.plot(deltaY)
	plt.xlabel("Command Number")
	plt.ylabel("Change in Y")
	plt.title("Swedish Wheel Travel Problem 3 - Change in Y vs Command Number")
	plt.show()

	plt.plot(deltaTheta)
	plt.xlabel("Command Number")
	plt.ylabel("Change in Theta")
	plt.title("Swedish Wheel Travel Problem 3 - Change in Theta vs Command Number")
	plt.show()
	print("----------Swedish Wheel Commands to Cover 5x5 Square----------")
	for command in commandList:
		print(command)
	ResetPositions()

	print("----------------------Problem 3 Response-----------------------")
	print("Changing from the Skid Steer model to the Swedish Wheel model \n" +
	"allows us to remove turning. A consequence to this is that we don't \n" +
	"need to issue as many commands, and we can utilize the whole area of \n" +
	"our robot. Some problems we might see is different motor powers for \n" +
	"the wheels, differing terrain, friciton, and the weight of the robot \n" +
	"changing actual distance traveled.")

# End Problem Functions #

def main():
	Problem1()
	Problem2()
	Problem3()

if __name__ == "__main__":
	main()
