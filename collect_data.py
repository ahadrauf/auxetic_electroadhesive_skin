import cv2
import numpy as np

# Create a black image and a window
windowName = 'MouseCallback'
cv2.namedWindow(windowName)
cv2.moveWindow(windowName, 40, 30)  # Move it to (40,30)

img = cv2.imread("./images/Half Locked Towards.jpg")
img = cv2.resize(img, (0, 0), fx=0.2, fy=0.2)

lst = []
homographyFinished = False
drawing = False

def distance_bottom_left(img, pt):
    h, w = np.shape(img)[:2]
    return np.linalg.norm(np.array([0, h]) - pt)

def distance_bottom_right(img, pt):
    h, w = np.shape(img)[:2]
    return np.linalg.norm(np.array([w, h]) - pt)
    
def sort_bottom_left_CCW(image, cnt):
    if len(cnt) == 0:
        return []
    return np.array([min(cnt, key=lambda pt: distance_bottom_left(image, pt)),
            min(cnt, key=lambda pt: distance_bottom_right(image, pt)),
            max(cnt, key=lambda pt: distance_bottom_left(image, pt)),
            max(cnt, key=lambda pt: distance_bottom_right(image, pt))])

def CallBackFunc(event, x, y, flags, param):
    global img, lst, homographyFinished, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        lst.append((x, y))
        print(x, y, lst)
        
    if len(lst) == 4 and not homographyFinished:
        h, w, _ = np.shape(img)
        ptsA = sort_bottom_left_CCW(img, lst)
        ptsB = np.array([[0, h], [w, h], [w, 0], [0, 0]])
        
        (H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)
        img = cv2.warpPerspective(img, H, (w, h))
        cv2.imshow(windowName, img)
        lst = []
        homographyFinished = True
        
    if drawing and event == cv2.EVENT_MOUSEMOVE:
        lst.append((x, y))
        print(len(lst))

def calculateCurvature():
    n = 50
    theta0 = np.arctan2(lst[n][1] - lst[0][1], lst[n][0] - lst[0][0])
    thetaf = np.arctan2(lst[-1][1] - lst[-1-n][1], lst[-1][0] - lst[-1-n][0])
    dtheta = ((thetaf - theta0) + np.pi) % (2*np.pi) - np.pi
    print(theta0, thetaf)
    print(dtheta, dtheta*180/np.pi)
    
    displacements = []
    for i in range(len(lst) - 1):
        displacements.append([lst[i+1][0] - lst[i][0], lst[i+1][1] - lst[i][1]])
        
    h, w, _ = np.shape(img)
    real_H, real_W = 21, 11 #52.2, 26.8 # cm
    displacements = [np.linalg.norm([x*real_W/w, y*real_H/h]) for (x, y) in displacements]
    s = sum(displacements)
    s *= 2.54
    print(s)
    K = dtheta/s
    print("Curvature (rad/cm):", K, 1/K)
        
# bind the callback function to window
cv2.setMouseCallback(windowName, CallBackFunc)

def main():
    while (True):
        cv2.imshow(windowName, img)
        key_input = cv2.waitKey(20) & 0xFF
        if key_input == 27 or key_input == ord('q'):  # escape or q
            break
        elif key_input == ord('n'):  # N
            print("pressed enter")
            calculateCurvature()
        elif key_input == ord('d'):
            global drawing
            drawing = not drawing
            
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()