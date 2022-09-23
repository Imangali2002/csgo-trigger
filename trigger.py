import cv2
import numpy as np
import pyautogui
import keyboard
from pynput.mouse import Controller as Controller
from pynput.mouse import Button
import time
from ctypes import windll, Structure, c_long, byref
import os
import winsound
from playsound import playsound
import threading

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}

# def playmusic():
#     playsound('ogon.mp3')

def playmusic2():
    freq = 200
    dur = 50
    for i in range(0, 3):    
        winsound.Beep(freq, dur)    
        freq+= 80
        dur+= 30

# start of the actual script
if __name__ == '__main__':
    print('Starting...')


    # setting up a view parameters
    mouse = Controller()
    enabledOneTab = False
    tm = int(round(time.time() * 1000))
    fps = 1
    fps1 = 0
    fpscounter = 0
    is_pressed_caps_lock = False

    while True:

        cur = queryMousePosition()

        img = pyautogui.screenshot(region=(cur['x']-5, cur['y']-5, 10, 10))
        img = np.array(img)
        frame = np.array(img).sum()

        if keyboard.is_pressed('caps_lock'):
            frame1 = np.array(img).sum()
            if enabledOneTab == True:
                thread2 = threading.Thread(target=playmusic2, args=())
                thread2.start()
                enabledOneTab = False
                thread2.join()
                continue
            else:
                print('Predicting...')
                winsound.Beep(30000, 100)
                time.sleep(0.3)
                winsound.Beep(30000, 120)
                enabledOneTab = True
            

        if enabledOneTab == True:
            if frame1 > (frame+500) or frame1 < (frame-500):
                # thread1 = threading.Thread(target=playmusic, args=())
                mouse.press(Button.left)
                # thread1.start()
                time.sleep(0.2)
                mouse.release(Button.left)
                keyboard.press('caps_lock')
                keyboard.release('caps_lock')
                enabledOneTab = False
                # thread1.join()
                continue
                #print('Shot')

            if frame1 > (frame+100) or frame1 < (frame-100):
                frame1 = np.array(img).sum()

        if int(round(time.time() * 1000))-tm > 1000:
            fps1 = fps
            tm = int(round(time.time() * 1000))
            fps = 0
        fps += 1
            
        r = 200.0 / img.shape[1]
        dim = (200, int(img.shape[0] * r))
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow("screenshot", img)
        if cv2.waitKey(1) == ord("q"):
            break
            cv2.destroyAllWindows()

        #print('colorValue: ' + str(frame) + ' FPS: ' + str(fps1))
        
        
        fpscounter += 1
        if fpscounter == 50:
            fpscounter = 0
            os.system('cls')
            print('FPS: ' + str(fps1))
