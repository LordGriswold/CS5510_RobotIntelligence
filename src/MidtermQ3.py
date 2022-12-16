from math import cos, radians, sin, sqrt, dist
import random
import time

def dx(t1, t4, t5, d3, d6):
	return (cos(t1)*cos(t4)*sin(t5)*d6) - (sin(t1)*cos(t5)*d6) - (sin(t1)*d3)

def dy(t1, t4, t5, d3, d6):
	return (sin(t1)*cos(t4)*sin(t5)*d6) + (cos(t1)*cos(t5)*d6) + (cos(t1)*d3)

def dz(t4, t5, d1, d2, d6):
	return d1 + d2 - (sin(t4)*sin(t5)*d6)

def ProblemA():
	x_goal = 1.2
	y_goal = 0.8
	z_goal = 0.5

	d1 = 0.2
	d2 = 0.5
	d3 = 1
	d6 = 0.2

	t1 = radians(-90)
	t4 = radians(-90)
	t5 = radians(90)
	t6 = radians(40)

	threshold = 0.05
	n = 10000

	# Initialize
	x = dx(t1, t4, t5, d3, d6)
	y = dy(t1, t4, t5, d3, d6)
	z = dz(t4, t5, d1, d2, d6)

	#Lets throw some darts
	for i in range(n):

		t1_diff = (random.random()-0.5)*.3
		t4_diff = (random.random()-0.5)*.3
		t5_diff = (random.random()-0.5)*.3

		d2_diff = (random.random()-0.5)*.3
		d3_diff = (random.random()-0.5)*.3

		t1_tmp = t1 + t1_diff
		t4_tmp = t4 + t4_diff
		t5_tmp = t5 + t5_diff

		d2_tmp = d2 + d2_diff
		d3_tmp = d3 + d3_diff

		# Ensure we don't have total negative extensions
		if (d2_tmp < 0 or d3_tmp < 0):
			pass

		# Calculate temporary x, y, and z values
		x_tmp = dx(t1_tmp, t4_tmp, t5_tmp, d3_tmp, d6)
		y_tmp = dy(t1_tmp, t4_tmp, t5_tmp, d3_tmp, d6)
		z_tmp = dz(t4_tmp, t5_tmp, d1, d2_tmp, d6)

		distance_current = dist([x, y, z], [x_goal, y_goal, z_goal])
		distance_tmp = dist([x_tmp, y_tmp, z_tmp], [x_goal, y_goal, z_goal])

		# Check to see if we have reached our goal
		if(abs(x_tmp - x_goal) < threshold and abs(y_tmp - y_goal) < threshold and abs(z_tmp - z_goal) < threshold):
			print(f"---------- Problem A Done in {i} loops -----------")
			print(f"Theta 1: {t1_tmp} rad")
			print(f"Theta 4: {t4_tmp} rad")
			print(f"Theta 5: {t5_tmp} rad")
			print(f"Theta 6: {radians(t6)} rad")
			print(f"Extension 1: {d1} m")
			print(f"Extension 2: {d2_tmp} m")
			print(f"Extension 3: {d3_tmp} m")
			print(f"Extension 6: {d6} m")
			print("----------------------------------------")
			break

		if(distance_current < distance_tmp):
			pass
		else:
			x = x_tmp
			y = y_tmp
			z = z_tmp
			t1 = t1_tmp
			t4 = t4_tmp
			t5 = t5_tmp
			d2 = d2_tmp
			d3 = d3_tmp

def isMinimalMovement(t1, d2, d3, t4, t5):
	return abs(t1) < abs(d2) < abs(d3) < abs(t4) < abs(t5)
	
def ProblemB():
	x_goal = 1.2
	y_goal = 0.8
	z_goal = 0.5

	d1 = 0.2
	d2 = 0.2
	d3 = 0.3
	d6 = 0.2

	t1 = radians(0)
	t4 = radians(-90)
	t5 = radians(90)
	t6 = radians(40)

	threshold = 0.05
	n = 20000

	# Initialize
	x = dx(t1, t4, t5, d3, d6)
	y = dy(t1, t4, t5, d3, d6)
	z = dz(t4, t5, d1, d2, d6)

	#Lets throw some darts
	for i in range(n):

		t1_diff = (random.random()-0.5)*.3
		t4_diff = (random.random()-0.5)*.3
		t5_diff = (random.random()-0.5)*.3

		d2_diff = (random.random()-0.5)*.3
		d3_diff = (random.random()-0.5)*.3

		t1_tmp = t1 + t1_diff
		t4_tmp = t4 + t4_diff
		t5_tmp = t5 + t5_diff

		d2_tmp = d2 + d2_diff
		d3_tmp = d3 + d3_diff

		# Ensure we don't have total negative extensions
		if (d2_tmp < 0 or d3_tmp < 0):
			pass

		# Calculate temporary x, y, and z values
		x_tmp = dx(t1_tmp, t4_tmp, t5_tmp, d3_tmp, d6)
		y_tmp = dy(t1_tmp, t4_tmp, t5_tmp, d3_tmp, d6)
		z_tmp = dz(t4_tmp, t5_tmp, d1, d2_tmp, d6)

		distance_current = dist([x, y, z], [x_goal, y_goal, z_goal])
		distance_tmp = dist([x_tmp, y_tmp, z_tmp], [x_goal, y_goal, z_goal])

		# Check to see if we have reached our goal
		if(abs(x_tmp - x_goal) < threshold and abs(y_tmp - y_goal) < threshold and abs(z_tmp - z_goal) < threshold):
			print(f"---------- Problem B Done in {i} loops -----------")
			print(f"Theta 1: {t1_tmp} rad")
			print(f"Theta 4: {t4_tmp} rad")
			print(f"Theta 5: {t5_tmp} rad")
			print(f"Theta 6: {radians(t6)} rad")
			print(f"Extension 1: {d1} m")
			print(f"Extension 2: {d2_tmp} m")
			print(f"Extension 3: {d3_tmp} m")
			print(f"Extension 6: {d6} m")
			print("----------------------------------------")
			break

		if(distance_current < distance_tmp or not isMinimalMovement(t1_diff, d2_diff, d3_diff, t4_diff, t5_diff)):
			pass
		else:
			x = x_tmp
			y = y_tmp
			z = z_tmp
			t1 = t1_tmp
			t4 = t4_tmp
			t5 = t5_tmp
			d2 = d2_tmp
			d3 = d3_tmp

def main():
	ProblemA()
	ProblemB()

if __name__ == "__main__":
	main()