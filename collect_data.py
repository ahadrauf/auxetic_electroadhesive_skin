import cv2
import numpy as np

# Create a black image and a window
windowName = 'MouseCallback'
cv2.namedWindow(windowName)
cv2.moveWindow(windowName, 40, 30)  # Move it to (40,30)

img = cv2.imread("./images/Unlocked without Skin.jpg")
img = cv2.resize(img, (0, 0), fx=0.2, fy=0.2)

lst = []

def CallBackFunc(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        lst.append((x, y))
        print(x, y)
#        print("Left button of the mouse is clicked - position (", x, ", ",y, ")")
#    elif event == cv2.EVENT_RBUTTONDOWN:
#        print("Right button of the mouse is clicked - position (", x, ", ", y, ")")
#    elif event == cv2.EVENT_MBUTTONDOWN:
#        print("Middle button of the mouse is clicked - position (", x, ", ", y, ")")
#    elif event == cv2.EVENT_MOUSEMOVE:
#        print("Mouse move over the window - position (", x, ", ", y, ")")
#    if flags == cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_LBUTTON:
#        print("Left mouse button is clicked while pressing CTRL key - position (", x, ", ",y, ")")
#    elif flags == cv2.EVENT_FLAG_RBUTTON + cv2.EVENT_FLAG_SHIFTKEY:
#        print("Right mouse button is clicked while pressing SHIFT key - position (", x, ", ", y, ")")
#    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_ALTKEY:
#        print("Mouse is moved over the window while pressing ALT key - position (", x, ", ", y, ")")
        
# bind the callback function to window
cv2.setMouseCallback(windowName, CallBackFunc)

def main():
    while (True):
        cv2.imshow(windowName, img)
        key_input = cv2.waitKey(20)
        if key_input == 27:  # escape
            break
        elif key_input == ord('enter'):
            print("pressed a")
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()