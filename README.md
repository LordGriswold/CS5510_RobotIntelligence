# CS5510 - **I**ntelligent (Robotics) **P**eter **E**than **E**athan **D**ave

## Project Submission

All project code can be found in `Project/`. Copies of the Yahboom motor and servo
code are located in `movement.py` and `servos.py`, and the final code used for the
video are in `CanDetection.py`. The detection model is included as `best.onnx` and 
a simplified version as `canSimplify.onnx`.

When executed on a Yahboom blue tank, the robot
will begin spinning to locate a can, then approach in short intervals. When a can
is detected a short distance in front of the robot, it will stop moving but
continue searching if the can is moved.

## Midterm Submission

Midterm sources are provided in `src/`, with a compiled version
supplied as `main.pdf`.
