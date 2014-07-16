#import serial, pygame.joystick
import pygame.joystick

# http://robotics.stackexchange.com/questions/2011/how-to-calculate-the-right-and-left-speed-for-a-tank-like-rover
def control_steering(thrust, theta):
	# assumes theta in degrees and thrust = -1 (100% rev) to 1 (100% fwd)
	# returns a tuple of percentages: (left_thrust [-1,1], right_thrust [-1,1])
	theta = ((theta + 180) % 360) - 180  # normalize value to [-180, 180)
	thrust = min(max(-1, thrust), 1)              # normalize value to [-1, 1]

	left = thrust*(theta/90.0 + 0.5);
	left = abs(left+1)-1;
	left = -(abs(-left+1)-1);

	right = thrust*(-theta/90.0 + 0.5);
	right = abs(right+1)-1;
	right = -(abs(-right+1)-1);
	return left,right

class KeyInput(object):
    def __init__(self, connection, up, down, left, right):
        self.x = 0
        self.y = 0
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.connection = connection

    def keyPressed(self,event):
        if event.keysym == 'Escape':
        	self.connection.close()
        	root.destroy()
        elif event.keysym == self.right:
            self.x = 0.5
        elif event.keysym == self.left:
            self.x = -0.5
        elif event.keysym == self.up:
            self.y = 1
        elif event.keysym == self.down:
            self.y = -1

    def keyReleased(self,event):
        if event.keysym == self.right:
            self.x = 0
        elif event.keysym == self.left:
            self.x = 0
        elif event.keysym == self.up:
            self.y = 0
        elif event.keysym == self.down:
            self.y = 0

    def task(self):
    	# calc wheels
    	#left = int((3 * self.y + self.x + 4) * 16)
    	#right = int((3 * self.y - self.x + 4) * 16)
    	left, right = control_steering(self.y, self.x*45)

    	# normalize and coerce [0,127]
    	left = int(left * 64 + 64)
    	right = int(right * 64 + 64)
    	left = min(max(0, left), 127)
    	right = min(max(0, right), 127)

    	# print and send
        print('x: ' + str(self.x) + '  y: ' + str(self.y) + '  left: ' + str(left) +
        	'  right: ' + str(right))
        if (self.y != 0) or (self.x != 0):
	        self.connection.write(str(unichr(left)) + str(unichr(right)) + str(unichr(0)))
        root.after(20,self.task)

class FakeSerial:
    """Fake Serial"""
    def write(self, str):
        print(str)       

# init joystick
pygame.joystick.init()
js = pygame.joystick.Joystick(0)

# config joystick
print("Wiggle steering")
steeringAxis = -1
while steeringAxis < 0: # wait for config
    for i in range(js.get_numaxes()): # check all axes
        if abs(js.get_axis()) > 0.5: # if value is more than a half
            steeringAxis = i # configure
print("Steering axis set as axis {}".format(steeringAxis))

print("Press go")
accBtn = -1
while accBtn < 0: # wait for config
    for i in range(js.get_numbuttons()): # check all axes
        if abs(js.get_button()) > 0.5: # if value is more than a half
            accBtn = i # configure
print("Acceleration button set as button {}".format(accBtn))

print("Press reverse")
revBtn = -1
while revBtn < 0: # wait for config
    for i in range(js.get_numbuttons()): # check all axes
        if abs(js.get_button()) > 0.5: # if value is more than a half
            revBtn = i # configure
print("Reverse button set as button {}".format(revBtn))

#bluetoothSerial = serial.Serial( "/dev/rfcomm1", baudrate=9600 )
bluetoothSerial = FakeSerial()


usr = KeyInput(bluetoothSerial, 'Up', 'Down', 'Left', 'Right')
root.bind_all('<Key>', usr.keyPressed)
root.bind_all('<KeyRelease>', usr.keyReleased)
root.after(20, usr.task)
root.mainloop()