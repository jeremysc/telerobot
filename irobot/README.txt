pyCreate is Brown's driver for the iRobot Create and is a thin Python wrapper
around the Create's Open Interface.

############################
Getting started:
############################

    Prerequisites: 
        
	pyCreate depends on python-serial ( http://pyserial.sourceforge.net )

	While the ROS wrapper for pyCreate will likely only run on Unix-like
	systems, pyCreate itself should work on all systems where Python and
	python-serial are available.

First, either append the location of the irobot directory to your PYTHONPATH or
otherwise make the module available to your python script.

from irobot import Create

will now import all the necessary functionality.

The essential functions are:

Create():
	Create() creates an object representing a robot attached to a particular
	serial port (which it accepts as its sole argument, e.g.
	Create("/dev/rfcomm0"). When no argument is given, "/dev/ttyUSB0" is
	assumed.

	To create a create name fred:

	fred = Create()

start():
	start() is necessary to make initial contact with the robot. start()
	should be called on a robot instance soon after it is created, and
	before any other calls are made.

stop():
	stop() is necessary to disconnect from the robot and to kill the threads
	used by the robot driver. Without a call to stop(), python scripts may
	not end cleanly or at all.

A simple Create life cycle is thus:

	fred = Create()
	fred.start()
	fred.stop()

The robot is controlled through six simple functions:

brake():
	stops the robot.

tank(right,left):
	sets the right and left wheel velocities. right and left are interpreted
	as mm/s and may range from -500 to 500.

forwardTurn(speed, radius):
	makes the robot arc. speed is a forward velocity between -500 and 500
	(interpreted in mm/s). radius is the radius of a circle the robot would
	inscribe if allowed to forwardTurn indefinitely. radius can vary between
	-2000 and 2000 and is interpreted as mm.

turn(speed):
	makes the robot turn in place (as opposed to following an arc) at speed.
	speed is interpreted in mm/s. Positive speed will result in a clockwise
	turn, negative speed a left.

right(speed):
	convenience function similar to turn. Robot will turn right (clockwise)
	at speed. 

left(speed):
	convenience function similar to turn. Robot will turn left
	(counter-clockwise) at speed.

There are two other functions:

demo(num):
	makes the robot enter demo number num (see the open interface manual).
	demo(255) will stop any running demo.

leds(play,advance,color,intensity):
	sets the robot's led states. play and advance are booleans. Their
	respective leds are set appropriately. color ranges from 0-255 0 being
	full green and 255 being red. This sets the color of the power led.
	intensity similarly ranges from 0-255 and sets the brightness of the
	power led.

Sensor data from the robot is available in the form of properties. For example,
given an instance of a robot stored in a variable named fred:

print fred.bumpLeft

will print 0 or 1 depending on the state of the left bumper. Properties
available this way include:

wheeldropCaster, wheeldropLeft, wheeldropRight, bumpLeft, bumpRight, wall,
cliffLeft, cliffFronLeft, cliffFrontRight, cliffRight, virtualWall,
infraredByte, advance, play, distance, angle, chargingState, voltage, current,
batteryTemperature, batteryCharge, batteryCapacity, wallSignal, cliffLeftSignal,
cliffFrontLeftSignal, cliffFrontRightSignal, cliffRightSignal, homeBase,
internalCharger, songNumber, and songPlaying

For details about these sensors, see the open interface documentation.

    Advanced control:

To facilitate maximum responsiveness, the pyCreate driver (as of v1.1) allows
you to register a function that will become part of the main sense-->act loop.
This function must take no arguments and is registered thusly:

def f():
	pass #your logic

fred = Create()
fred.update = f
fred.start()

Such a function can *only* be registered when the driver is not running (i.e.
before the first call to start or between a call to reset and start). Keep in
mind that this function becomes part of the main loop. If the function takes too
long to execute the refresh rate of the robot may drop below 15Hz. 
