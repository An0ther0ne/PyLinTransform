import numpy as np
import cv2 

# --- Global Vars

WND_CAPTION = "Linear transformations"
SIZE_X 		= 800
SIZE_Y 		= 300
PAD_Y       = 10
SHIFT_Y 	= 3 * SIZE_Y // 8
Y0 			= SIZE_Y // 2
X0			= SIZE_X // 2
WIDTH		= 5
CHANGED		= True
POINTS		= 500
COLOR_MIN	= 32
COLOR_MAX	= 255
TEXT_COLOR	= 255
ZOOM_COEF 	= 19/20
CURRENT_FUNCTION = 0

# --- Lambda Functions set

FUNCTIONS = {
	'1+1/x' :lambda x:0 if x==0 else 1+1/x,
	'x^2'   :lambda x:x**2,
	'sin(x)':lambda x:np.sin(3*x),
	'tan(x)':lambda x:np.tan(3*x),
}

# --- Procedures

def Draw(input_frame):
	global FUNCTIONS, CURRENT_FUNCTION
	def projectionx(n):
		return int(X0 + X0 * n / WIDTH)
	frame  = np.copy(input_frame)
	y1 = PAD_Y
	y2 = SIZE_Y - PAD_Y
	for i, in_x in enumerate(input_x):
		x1 = projectionx(in_x)
		print(CURRENT_FUNCTION, flush=True)
		x2 = projectionx(list(FUNCTIONS.values())[CURRENT_FUNCTION](in_x))
		color = int(COLOR_MIN + i * (COLOR_MAX - COLOR_MIN)/len(input_x))
		if abs(x2) < 2*SIZE_X:
			frame = cv2.line(frame, (x1,y1), (x2,y2), (color), 1)
	return frame
	
def mouse_evnt(event, x, y, flags, param):
	global WIDTH, CHANGED, CURRENT_FUNCTION
	if event == 10:					# scroll
		CHANGED = True
		if 	 flags > 0:				# Up
			WIDTH *= ZOOM_COEF
		elif flags < 0: 			# Down
			WIDTH /= ZOOM_COEF
		else:
			CHANGED = False
	elif event == 1 or event == 2:	# left/right click
		CHANGED = True
		CURRENT_FUNCTION = (CURRENT_FUNCTION + 1) % len(FUNCTIONS)
	
input_x = np.arange(-WIDTH, WIDTH, 2 * WIDTH/POINTS)
blank_screen = np.zeros((SIZE_Y, SIZE_X), dtype=np.uint8) # Gray scale

# --- Main Cycle

while True:
	if CHANGED:
		CHANGED = False
		Caption = list(FUNCTIONS.keys())[CURRENT_FUNCTION]
		cv2.imshow(WND_CAPTION, 
			cv2.putText(cv2.putText(cv2.putText(cv2.putText(Draw(blank_screen),
			"ESC - Quit", (5,10), cv2.FONT_HERSHEY_SIMPLEX, 1/3, (TEXT_COLOR), 1),
			"Any key - Next", (5,20), cv2.FONT_HERSHEY_SIMPLEX, 1/3, (TEXT_COLOR), 1),
			"Mouse Scroll - Zoom", (5,30), cv2.FONT_HERSHEY_SIMPLEX, 1/3, (TEXT_COLOR), 1),
			Caption, (SIZE_X - 50,SIZE_Y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1/3, (TEXT_COLOR), 1)
		)
		cv2.setMouseCallback(WND_CAPTION, mouse_evnt)
	key = cv2.waitKey(2) & 0xFF
	if  key | 0x20 == ord('q') or key == 27: # 'q' or 'Q ' or 'ESC'
		break
	elif key != 255:
		print("+++ Key = {}".format(key), flush=True)
		CURRENT_FUNCTION = (CURRENT_FUNCTION + 1) % len(FUNCTIONS)
		CHANGED = True
cv2.destroyAllWindows()
