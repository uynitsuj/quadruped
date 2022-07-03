## Justin Yu's Custom Quadruped
Inspired by Boston Dynamics' Spot Mini, MIT's Mini Cheetah, and the exceptional work by my good friend Adham Elarabawy on OpenQuadruped <br> https://www.adham-e.dev/<br> https://github.com/adham-elarabawy/open-quadruped

<img src="https://raw.githubusercontent.com/uynitsuj/quadruped/main/img/QPRev2.png?raw=true" height="100%" width="100%">

**Mechanical**: I'll be starting out with a lightweight but robust 3D Printed frame + some fairly powerful hobby servos with a BOM cost of <$800.
Eventually, I hope to scale it up and move to hobby brushless DC motors. Or in the far future, custom motor technology.

**Control**: I'm using a Raspberry Pi for pose computation and a Teensy 4.0 MCU to handle peripheral IO but mainly PWM to the servo motors. In the far future I might scale to a Nvidia Jetson Nano SOM for more complex motion/path planning projects, which would require a much better sensor suite.

**Demos**
<img src="https://github.com/uynitsuj/quadruped/blob/main/img/QIKstress.gif?raw=true" height="100%" width="100%">
<img src="https://github.com/uynitsuj/quadruped/blob/main/img/legdemo.gif?raw=true" height="60%" width="60%">
<img src="https://github.com/uynitsuj/quadruped/blob/main/img/ezgif-3-fced31d97cb5.gif?raw=true" height="60%" width="60%">



### To-Do List

- [ ] *Hardware & Software* // Untethered operation with joystick pose control
- [ ] *Hardware* // Research current sense circuit for contact detection
- [ ] *Software* // Rewrite controller code in C++
- [ ] *Software* // Change power-on servo initialization angles
- [ ] *Software* // Physics Simulation
- [ ] *Software* // Walking
