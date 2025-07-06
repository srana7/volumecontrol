import cv2
import mediapipe as mp
import pyautogui
x1 = y1 = x2 = y2 = 0 #for 1 line between finger, co-ordinate

webcam = cv2.VideoCapture(0)  #0 is the no. of webcam. here we took 1 webcam so
#create 2 object to capture hand & to draw points on hand
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    _ , image = webcam.read() #capture image, give 2 variable. we take only one i.e image so other one is _
    image = cv2.flip(image,1)
    frame_height, frame_width ,_ = image.shape # height , width and depth

    rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) # rgb converted
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image,hand)
            landmarks = hand.landmark # thumb & fore finger landmark collecting
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8: # fore finger's landmark is 8
                    cv2.circle(img=image,center=(x,y),radius=8,color=(255,0,0),thickness=3) # draw circle in forefinger
                    x1 = x
                    y1 = y
                if id == 4: # thumb finger's landmark is 4
                    cv2.circle(img=image,center=(x,y),radius=8,color=(0,0,255),thickness=3) # draw circle in thumb, red
                    x2 = x
                    y2 = y
        dist = ((x2-x1)**2 + (y2-y1)**2)**(0.5)//4 #dist formula. the value is betn 0 to 100 o div by 4 so that 0-35
        cv2.line(image,(x1,y1),(x2,y2),(0,255,0),5)
        if dist > 20 :
            pyautogui.press("volumeup")
        else :
            pyautogui.press("volumedown")

    cv2.imshow("Hand volume control using python", image)  # shoe vdo in window
    key = cv2.waitKey(10)#continous loop 10 milisec
    if key == 27:
        break
pyautogui.FAILSAFE = False
webcam.release()
cv2.destroyAllWindows()
