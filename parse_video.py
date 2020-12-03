import cv2
import numpy as np
import csv

# Create a black image and a window
windowName = 'MouseCallback'
cv2.namedWindow(windowName)
cv2.moveWindow(windowName, 40, 30)  # Move it to (40,30)

# img = cv2.imread("./images/Half Locked Towards.jpg")
img = None

lst = []
basePt = []
lastPt = []
distances = []
H = None
homographyFinished = False
drawing = False
h = 0
w = 0

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
    global img, lst, homographyFinished, drawing, h, w
    if event == cv2.EVENT_LBUTTONDOWN:
        if homographyFinished:
            real_H, real_W = 21*2.54, 11*2.54 #52.2, 26.8 # cm
            x = x*real_W/w
            y = y*real_H/h
        lst.append((x, y))
        print(x, y, lst)
        
    if len(lst) == 4 and not homographyFinished:
        global H, basePt
        h, w, _ = np.shape(img)
        ptsA = sort_bottom_left_CCW(img, lst[:4])
        ptsB = np.array([[0, h], [w, h], [w, 0], [0, 0]])
        
        (H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)
        img = cv2.warpPerspective(img, H, (w, h))
        cv2.imshow(windowName, img)
        lst = []
        homographyFinished = True
        
# bind the callback function to window
cv2.setMouseCallback(windowName, CallBackFunc)

def main():
    vid = cv2.VideoCapture('videos/20201129_175047_mylar_test3.mp4')

    currentFrame = 0
    global img
    skip = 3
    while (vid.isOpened()):
        ret, img = vid.read()
        if (currentFrame % skip != 0):   
            currentFrame += 1
            continue
        # img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE) 
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print('Frame', currentFrame)
        img = cv2.resize(img, (0, 0), fx=0.4, fy=0.4)
        if homographyFinished:
            img = cv2.warpPerspective(img, H, (w, h))
    
        cv2.imshow(windowName, img)
        key_input = cv2.waitKey(0) & 0xFF
        if key_input == 27 or key_input == ord('q'):  # escape or q
            break
        elif key_input == ord('n'):  # N
            global lst, basePt, lastPt, distances
            if len(lst) == 2:
                basePt = lst[0]
                distance = np.linalg.norm([lst[1][0] - basePt[0], lst[1][1] - basePt[1]])
                distances.append([currentFrame / 30., distance])
                lastPt = lst[1]
                lst = []
            elif len(lst) == 1:
                distance = np.linalg.norm([lst[0][0] - basePt[0], lst[0][1] - basePt[1]])
                distances.append([currentFrame / 30., distance])
                lastPt = lst[0]
                lst = []
            elif len(lst) == 0:
                distance = np.linalg.norm([lastPt[0] - basePt[0], lastPt[1] - basePt[1]])
                distances.append([currentFrame / 30., distance])
            print(distance)
                
        elif key_input == ord('s'):
            # field names
            print(distances)
            fields = ['Time (s)', 'Distance (cm)']
                
            # name of csv file  
            filename = "t_vs_x_mylar.csv"
                
            # writing to csv file  
            with open(filename, 'w') as csvfile:  
                # creating a csv writer object  
                csvwriter = csv.writer(csvfile)  
                    
                # writing the fields  
                csvwriter.writerow(fields)  
                    
                # writing the data rows  
                csvwriter.writerows(distances)
                
        currentFrame += 1
            
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()