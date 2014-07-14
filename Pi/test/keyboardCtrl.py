import lightblue, Tkinter as tk, pygame

class fakeBT(object):
	"""fakeBT - A fake lightblue socket connection"""
	def __init__(self):
		super(fakeBT, self).__init__()

	def send(self, string):
		print(str(string))

	def close(self):
		print('ended fakeBT')

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
	        self.connection.send(str(unichr(left)) + str(unichr(right)) + str(unichr(0)))
        root.after(20,self.task)

root = tk.Tk()

dev = lightblue.selectservice()
print(dev[0])

socket = lightblue.socket()
socket.connect((dev[0], dev[1]))
socket.send(str(unichr(2)))
#socket = fakeBT()

usr = KeyInput(socket, 'Up', 'Down', 'Left', 'Right')
root.bind_all('<Key>', usr.keyPressed)
root.bind_all('<KeyRelease>', usr.keyReleased)
root.after(20, usr.task)
root.mainloop()