import cv2
import numpy as np
import pyautogui
import mediapipe as mp
from tkinter import *
from tkinter import filedialog

# Gesture to action mapping
gesture_mapping = {
    'Palm': 'Mouse Move',
    'I': 'Left Click',
    'Fist': 'Right Click',
    'OK': 'Scroll Up',
    'C': 'Scroll Down',
    'Thumb': 'Space',
    'Index': 'Enter',
    'Thumb_Up': 'Like Action',
    'Thumb_Down': 'Dislike Action',
    'Peace_Sign': 'Peace Action',
    'Pinch': 'Pinch Action',
    'Fist': 'Close the Application',
    'Open_Hand': 'Minimize Window',
    'Thumb_to_Pinky': 'Maximize Window',
    'Okay': 'Take Screenshot',
    'Zoom_In': 'Zoom In Action',
    'Zoom_Out': 'Zoom Out Action',
    'Left_Swipe': 'Left Swipe Action',
    'Right_Swipe': 'Right Swipe Action'
}

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Perform action based on detected gesture
def perform_action(gesture):
    if gesture == "left_swipe":
        pyautogui.hotkey('ctrl', 'left')  # Simulate left swipe
    elif gesture == "right_swipe":
        pyautogui.hotkey('ctrl', 'right')  # Simulate right swipe
    elif gesture == "zoom_in":
        pyautogui.hotkey('ctrl', '+')  # Zoom in
    elif gesture == "zoom_out":
        pyautogui.hotkey('ctrl', '-')  # Zoom out
    elif gesture == "click":
        pyautogui.click()  # Simulate mouse click
    elif gesture == "thumb_up":
        print("Thumb Up Detected - Like Action")
    elif gesture == "thumb_down":
        print("Thumb Down Detected - Dislike Action")
    elif gesture == "peace_sign":
        print("Peace Sign Detected")
    elif gesture == "pinch":
        print("Pinch Detected")
    elif gesture == "fist":
        print("Fist Detected - Close the Application")
        exit()  # Close the application on Fist gesture
    elif gesture == "open_hand":
        print("Open Hand Detected - Minimize Window")
        pyautogui.hotkey('win', 'down')  # Minimize window
    elif gesture == "thumb_to_pinky":
        print("Thumb to Pinky Detected - Maximize Window")
        pyautogui.hotkey('win', 'up')  # Maximize window
    elif gesture == "okay":
        print("Okay Detected - Take Screenshot")
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")  # Save the screenshot

# Function to detect advanced gestures
def detect_advanced_gesture(landmarks):
    wrist = landmarks[0]
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    gesture = "none"

    # Thumb Up Gesture (Thumb pointing upwards)
    if thumb_tip.y < wrist.y and abs(thumb_tip.x - wrist.x) < 0.1:
        gesture = "thumb_up"
    
    # Thumb Down Gesture (Thumb pointing downwards)
    elif thumb_tip.y > wrist.y and abs(thumb_tip.x - wrist.x) < 0.1:
        gesture = "thumb_down"

    # Peace Sign Gesture (Index and middle fingers extended)
    elif abs(index_tip.y - middle_tip.y) < 0.05 and abs(index_tip.x - middle_tip.x) < 0.05 and thumb_tip.y < wrist.y:
        gesture = "peace_sign"
    
    # Pinch Gesture (Thumb and index finger close together)
    elif abs(thumb_tip.x - index_tip.x) < 0.05 and abs(thumb_tip.y - index_tip.y) < 0.05:
        gesture = "pinch"

    # Fist Gesture (All fingers curled)
    elif (thumb_tip.y > wrist.y and index_tip.y > wrist.y and middle_tip.y > wrist.y and 
          ring_tip.y > wrist.y and pinky_tip.y > wrist.y):
        gesture = "fist"

    # Open Hand Gesture (All fingers extended)
    elif (thumb_tip.y < wrist.y and index_tip.y < wrist.y and middle_tip.y < wrist.y and 
          ring_tip.y < wrist.y and pinky_tip.y < wrist.y):
        gesture = "open_hand"

    # Thumb to Pinky Gesture (Thumb touching pinky)
    elif abs(thumb_tip.x - pinky_tip.x) < 0.05 and abs(thumb_tip.y - pinky_tip.y) < 0.05:
        gesture = "thumb_to_pinky"

    # Okay Gesture (Thumb and index finger forming a circle)
    elif abs(thumb_tip.x - index_tip.x) < 0.05 and abs(thumb_tip.y - index_tip.y) < 0.05:
        gesture = "okay"

    # Zoom In Gesture (Thumb and index finger spreading apart)
    elif abs(thumb_tip.x - index_tip.x) > 0.1 and abs(thumb_tip.y - index_tip.y) > 0.1:
        gesture = "zoom_in"
    
    # Zoom Out Gesture (Thumb and index finger closing together)
    elif abs(thumb_tip.x - index_tip.x) < 0.05 and abs(thumb_tip.y - index_tip.y) < 0.05:
        gesture = "zoom_out"

    # Left Swipe Gesture (Hand moving to the left)
    if index_tip.x < thumb_tip.x and pinky_tip.x < index_tip.x:
        gesture = "left_swipe"
    
    # Right Swipe Gesture (Hand moving to the right)
    if index_tip.x > thumb_tip.x and pinky_tip.x > index_tip.x:
        gesture = "right_swipe"

    return gesture

# Real-time webcam gesture prediction
def webcamPredict():
    cap = cv2.VideoCapture(0)  # 0 for the default webcam
    
    last_predicted_gesture = None  # Track previous gesture to avoid repetition
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip the frame horizontally for mirror effect
        img = cv2.flip(frame, 1)
        
        # Convert the frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)
        
        # Check if hands are detected
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get the gesture from hand landmarks
                gesture = detect_advanced_gesture(hand_landmarks.landmark)

                # Perform action if a valid gesture is detected
                if gesture != "none" and gesture != last_predicted_gesture:
                    last_predicted_gesture = gesture
                    perform_action(gesture)
                
                # Display detected gesture on the frame
                cv2.putText(img, f"{gesture}", 
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the processed frame
        cv2.imshow("Hand Gesture Recognition", img)
        
        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# GUI Components
main = Tk()
main.title("Hand Gesture Recognition")
main.geometry("1300x1200")
font1 = ('times', 14, 'bold')
predictButton = Button(main, text="Recognize Gesture from Webcam", command=webcamPredict)
predictButton.place(x=50, y=100)
predictButton.config(font=font1)

main.mainloop()

