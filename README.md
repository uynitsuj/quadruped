## Justin Yu's Custom Quadruped
For this custom quadrupedal robot project, my high-level design goals and objectives are:

* Scalability (?) Quadrupedal Platform
* **Platform** (put down twice out of importance)
* Reproducible by others from following my work/documentation

Lower Level:
**Mechanical**: I'll be starting out with a small scale 3D Printed frame + some fairly powerful hobby servos with a BOM cost of <$600. Servos seem like a decent closed-loop solution to start out with for rudimentary pose acquisition as a baseline.
Eventually, I hope to scale it up and move to hobby brushless DC motors. I am also currently in the Michigan Mars Rover Robotic Arm subteam where they are developing custom BLDC motor controllers and motors, I'll have to take a couple of notes, and then later, I might find interest in developing custom actuator technology for Michigan like Ben Katz did for MIT in the far far future.
**Control**: If I spend enough time with the hobby servos and like them enough, I might expand the control system to include force sensitive feet or implement force feedback on the servos with some hall effect sensors or something similar, since servos don't have that capability on their own.
I'll probably be starting out with an Raspberry Pi for pose computation and a Teensy 4.0 to handle PWM to the servos. In the far future I might scale to a Nvidia Jetson Nano for more complex gait/motion/path planning projects. (edited) 

Some short term tasks & milestones:
* I recently solved quadruped Inverse Kinematics for one leg, next step for me is to verify the model and write up a python visualization for full quadruped static pose acquisition
* CAD Mk1 leg - I hope to get this finished before I head home for break so I can hopefully start printing some prototypes and get a leg testbench going
