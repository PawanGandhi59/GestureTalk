import threading
import tkinter as tk
from tkinter import scrolledtext
import cv2
import mediapipe as mp
import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import numpy as np
import wmi
import math
import time
import keyboard
import speech_recognition as sr
import queue
import google.generativeai as genai
import subprocess

# ========== Gemini Setup ==========
genai.configure(api_key="AIzaSyA6pjpwQEB6eVVTCNisqYLQLwSlt_aI-Qs")  # Replace with your key
model = genai.GenerativeModel("gemini-2.5-pro")
chat = model.start_chat()

# ========== Voice Assistant ==========
def voice_assistant():

    def listen_for_audio(recognizer, microphone, audio_queue):
        with microphone as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source)
            print("Start speaking...")

            while True:
                try:
                    audio = recognizer.listen(source)
                    audio_queue.put(audio)  

                except sr.UnknownValueError:
                    print("Sorry, I didn't understand that.")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                except KeyboardInterrupt:
                    print("Stopping audio capture.")
                    break


    def recognize_speech(recognizer, audio_queue, language="en-US"):
        c=0
        newfile = ["hey", "jarvis", "open", "new", "file"]
        file = ["hey", "jarvis", "open", "existing", "file"]
        closefile=["hey", "jarvis", "close", "file"]
        youtube = ["hey", "jarvis", "open", "youtube"]
        closeyoutube=["hey", "jarvis", "close", "youtube"]
        chrome = ["hey", "jarvis", "open", "chrome"]
        closechrome=["hey","jarvis","close","chrome"]
        calculator = ["hey", "jarvis", "open", "calculator"]
        closecalculator=["hey", "jarvis", "close", "calculator"]
        replace=["hey","jarvis","replace"]
        nf=" "

        while True:
            if not audio_queue.empty():  
                audio = audio_queue.get()  

                try:
                    print(f"Recognizing in {language}...")
                    text = recognizer.recognize_google(audio, language=language)
                    print(f"You said: {text}")
                
               
                    if all(word in text.lower() for word in newfile):
                        c=1
                        a=input("Enter name of file:")
                        nf=open(f"{a}.txt",'w+')
                        print("file opened succesfully,")
                        print("Do not forget to close the file by saying hey jarvis close file")

                    elif all(word in text.lower() for word in file):
                        c=2
                        b=input("Enter name of file you want to open:")
                        try:
                            nf=open(f"{b}.txt",'a+')
                            print("Existing file opened succesfully")
                            print("Do not forget to close the file by saying hey jarvis close file")
                        except Exception:
                            print("File not found or file does not exist")

                    elif all(word in text.lower()for word in closefile):
                        if c!=0:
                            nf.close()
                            c=0
                            print("file closed")
                        else:
                            print("No file to close")
                  
                    if all(word in text.lower() for word in youtube):
                        subprocess.Popen(['chrome', 'https://www.youtube.com'])
                        print("Opening YouTube...")

                    if all(word in text.lower() for word in closeyoutube):
                        subprocess.run(['taskkill', '/F', '/IM','chrome.exe' ])
                        print("youtube closed")

                    if all(word in text.lower() for word in chrome):
                        subprocess.run('chrome')
                        print("Opening Chrome...")

                    if all(word in text.lower() for word in closechrome):
                        subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'])
                        print("chrome closed")

                    if all(word in text.lower() for word in calculator):
                        subprocess.run('calc')
                        print("Opening Calculator...")

                    if all(word in text.lower() for word in closecalculator):
                      subprocess.run(['taskkill', '/F', '/IM', 'CalculatorApp.exe'])
                      print("Calculator closed")

                    if all(word in text.lower() for word in replace):
                        if c!=0:
                            z=input("Enter word to replace:")
                            x=input("Enter new word to replace old word with")
                            nf.seek(0)
                            content=nf.read()
                            if z in content:
                                ucontent=content.replace(z,x)
                                nf.seek(0)
                                nf.truncate()
                                nf.write(ucontent)
                            else:
                                print("No such word found in file")

                        else:
                            print("No file open to perform replace operation")

                    if c==1:
                        nf.write(text+" ")
                
                    elif c==2:
                        nf.write(" "+text)
                except sr.UnknownValueError:
                    print("Sorry, I didn't understand that.")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")


    audio_queue = queue.Queue()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    listen_thread = threading.Thread(target=listen_for_audio, args=(recognizer, microphone, audio_queue))
    listen_thread.daemon = True
    listen_thread.start()

       
    recognize_thread = threading.Thread(target=recognize_speech, args=(recognizer, audio_queue))
    recognize_thread.daemon = True
    recognize_thread.start()

        
    listen_thread.join()
    recognize_thread.join()


# ========= Gesture Control ==========
def gesture_control():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
    draw = mp.solutions.drawing_utils

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    min_vol, max_vol = volume.GetVolumeRange()[0:2]

    brightness_controller = wmi.WMI(namespace='wmi')
    brightness_methods = brightness_controller.WmiMonitorBrightnessMethods()[0]
    brightness_level = brightness_controller.WmiMonitorBrightness()[0].CurrentBrightness

    screen_w, screen_h = pyautogui.size()
    pyautogui.FAILSAFE = False

    prev_right_y = prev_left_y = None
    last_music_toggle_time = 0
    MUSIC_COOLDOWN = 1.5
    last_minimize_time = 0
    MINIMIZE_COOLDOWN = 2.0
    last_tab_switch = 0
    alt_tab_active = False
    last_right_click_time = 0
    RIGHT_CLICK_COOLDOWN = 0.5
    last_close_time = 0
    CLOSE_COOLDOWN = 2.0

    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_img)
        right_hand = left_hand = None

        if result.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                label = handedness.classification[0].label
                lm_list = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]
                fingers_up = [lm_list[i][1] < lm_list[i - 2][1] for i in [8, 12, 16, 20]]
                all_up = all(fingers_up)
                wrist_y = lm_list[0][1]

                if label == "Right":
                    right_hand = lm_list
                    if all_up:
                        if prev_right_y is not None:
                            dy = prev_right_y - wrist_y
                            if abs(dy) > 5:
                                current_vol = volume.GetMasterVolumeLevel()
                                new_vol = np.clip(current_vol + dy * 0.1, min_vol, max_vol)
                                volume.SetMasterVolumeLevel(new_vol, None)
                                vol_display = int(np.interp(new_vol, [min_vol, max_vol], [0, 100]))
                                cv2.putText(img, f'Volume: {vol_display}%', (10, 50),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        prev_right_y = wrist_y
                    else:
                        prev_right_y = None

                    index_up = lm_list[8][1] < lm_list[6][1]
                    middle_up = lm_list[12][1] < lm_list[10][1]
                    if index_up and middle_up:
                        x, y = lm_list[8]
                        x = np.clip(x, 50, w - 50)
                        y = np.clip(y, 50, h - 50)
                        screen_x = np.interp(x, [50, w - 50], [0, screen_w])
                        screen_y = np.interp(y, [50, h - 50], [0, screen_h])
                        pyautogui.moveTo(screen_x, screen_y, duration=0.05)

                    thumb, index, pinky = lm_list[4], lm_list[8], lm_list[20]
                    if math.hypot(thumb[0] - pinky[0], thumb[1] - pinky[1]) < 40 and time.time() - last_music_toggle_time > MUSIC_COOLDOWN:
                        pyautogui.press('playpause')
                        last_music_toggle_time = time.time()

                    middle = lm_list[12]
                    if math.hypot(thumb[0] - middle[0], thumb[1] - middle[1]) < 30 and time.time() - last_music_toggle_time > MUSIC_COOLDOWN:
                        pyautogui.press('nexttrack')
                        last_music_toggle_time = time.time()

                    if math.hypot(thumb[0] - index[0], thumb[1] - index[1]) < 30 and time.time() - last_right_click_time > RIGHT_CLICK_COOLDOWN:
                        pyautogui.rightClick()
                        last_right_click_time = time.time()

                    rock = all([lm_list[i][1] > lm_list[i - 2][1] for i in [8, 12, 16, 20]])
                    if rock and time.time() - last_minimize_time > MINIMIZE_COOLDOWN:
                        pyautogui.hotkey('win', 'down')
                        last_minimize_time = time.time()

                    if math.hypot(thumb[0] - lm_list[16][0], thumb[1] - lm_list[16][1]) < 40:
                        if not alt_tab_active:
                            keyboard.press('alt')
                            alt_tab_active = True
                            last_tab_switch = time.time()
                        elif time.time() - last_tab_switch > 0.7:
                            keyboard.press_and_release('tab')
                            last_tab_switch = time.time()
                    elif alt_tab_active:
                        keyboard.release('alt')
                        alt_tab_active = False

                elif label == "Left":
                    left_hand = lm_list
                    if all_up:
                        if prev_left_y is not None:
                            dy = wrist_y - prev_left_y
                            if abs(dy) > 5:
                                if dy < 0 and brightness_level < 100:
                                    brightness_level = min(100, brightness_level + 2)
                                elif dy > 0 and brightness_level > 0:
                                    brightness_level = max(0, brightness_level - 2)
                                brightness_methods.WmiSetBrightness(brightness_level, 0)
                                cv2.putText(img, f'Brightness: {brightness_level}%', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                        prev_left_y = wrist_y
                    else:
                        prev_left_y = None

                    thumb, index, middle, ring = lm_list[4], lm_list[8], lm_list[12], lm_list[16]
                    if math.hypot(thumb[0] - index[0], thumb[1] - index[1]) < 30:
                        pyautogui.click()
                        time.sleep(0.3)
                    if math.hypot(thumb[0] - ring[0], thumb[1] - ring[1]) < 30:
                        pyautogui.doubleClick()
                        time.sleep(0.4)
                    if math.hypot(thumb[0] - middle[0], thumb[1] - middle[1]) < 30 and time.time() - last_music_toggle_time > MUSIC_COOLDOWN:
                        pyautogui.press('prevtrack')
                        last_music_toggle_time = time.time()

                draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if right_hand and left_hand:
            r_index, l_index = right_hand[8], left_hand[8]
            r_middle, l_middle = right_hand[12], left_hand[12]
            if math.hypot(r_index[0] - l_index[0], r_index[1] - l_index[1]) < 30:
                if math.hypot(r_middle[0] - l_middle[0], r_middle[1] - l_middle[1]) < 30:
                    if time.time() - last_close_time > CLOSE_COOLDOWN:
                        pyautogui.hotkey('alt', 'f4')
                        last_close_time = time.time()
                elif math.hypot(r_middle[0] - l_middle[0], r_middle[1] - l_middle[1]) > 60:
                    if time.time() - last_close_time > CLOSE_COOLDOWN:
                        pyautogui.hotkey('win', 'up')
                        last_close_time = time.time()

        cv2.imshow("Gesture Control", img)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# ========== Gemini Chat GUI ==========
def start_gui():
    root = tk.Tk()
    root.title("Gemini Chat Assistant")
    root.geometry("500x500")

    chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=("Segoe UI", 10))
    chat_area.pack(padx=10, pady=10)
    chat_area.configure(state='disabled')

    input_frame = tk.Frame(root)
    input_frame.pack(fill='x', padx=10)

    user_input = tk.Entry(input_frame, font=("Segoe UI", 10), width=40)
    user_input.pack(side='left', fill='x', expand=True, padx=(0, 5))

    def send():
        query = user_input.get()
        if query.strip() == "":
            return
        chat_area.configure(state='normal')
        chat_area.insert(tk.END, "You: " + query + "\n")
        chat_area.configure(state='disabled')
        user_input.delete(0, tk.END)

        try:
            response = chat.send_message(query)
            reply = response.text.strip()
        except Exception as e:
            reply = f"[Gemini Error]: {str(e)}"

        chat_area.configure(state='normal')
        chat_area.insert(tk.END, "Gemini: " + reply + "\n\n")
        chat_area.configure(state='disabled')
        chat_area.yview(tk.END)

    send_btn = tk.Button(input_frame, text="➤", font=("Segoe UI", 12), width=4, command=send)
    send_btn.pack(side='right')

    user_input.bind("<Return>", lambda event: send())

    threading.Thread(target=voice_assistant, daemon=True).start()

    root.mainloop()

# ========== Main ==========
if __name__ == "__main__":
    threading.Thread(target=start_gui, daemon=True).start()
    gesture_control()
