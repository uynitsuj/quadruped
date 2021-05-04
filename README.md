## Justin Yu's Custom Quadruped
Inspired by Boston Dynamics' Spot Mini, MIT's Mini Cheetah, and the exceptional work by my good friend Adham Elarabawy on OpenQuadruped <br> https://www.adham-e.dev/<br> https://github.com/adham-elarabawy/open-quadruped
<img src="https://raw.githubusercontent.com/uynitsuj/quadruped/main/img/QPRev2.png?raw=true" height="100%" width="100%">
<img src="https://github.com/uynitsuj/quadruped/blob/main/img/QIKstress.gif?raw=true" height="100%" width="100%">

**Mechanical**: I'll be starting out with a small scale 3D Printed frame + some fairly powerful hobby servos with a BOM cost of <$800.
Eventually, I hope to scale it up and move to hobby brushless DC motors. Or in the far future, custom motor technology perhaps.

**Control**: If I spend enough time with the hobby servos and like them enough, I might expand the control system to include force sensitive feet or implement force feedback on the servos with some hall effect sensors or something similar, since servos don't have that capability on their own.
I'll start out with a Raspberry Pi for pose computation and a Teensy 4.0 to handle PWM to the servos. In the far future I might scale to a Nvidia Jetson Nano for more complex gait/motion/path planning projects.
