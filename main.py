import cv2
import mediapipe as mp
import serial.tools.list_ports
import warnings
import time
import threading

# ...

def write_to_serial(message):
    message_bytes = bytes(message, 'utf-8')  # Convert string to bytes
    serialInst.write(message_bytes)
    print("Message sent to Arduino: ", message_bytes)

warnings.filterwarnings('ignore', category=UserWarning)
z=1
try:
    ports=serial.tools.list_ports.comports()
    serialInst = serial.Serial()
    portsList = []

    for one in ports :
       portsList.append(str(one))
     

    serialInst.baudrate = 9600
    serialInst.port = 'COM8'
    serialInst.open()
    print("Arduino Connected Successfully")
except :
    print("Arduino not Connected")
else:
    z=0

# Initialize hand tracking module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open video capture
cap = cv2.VideoCapture(0)

while True:
    # Read frame from video capture
    ret, frame = cap.read()
    
    # Convert frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process frame with hand tracking
    results = hands.process(frame_rgb)
    
    # Draw hand landmarks on frame
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, landmark in enumerate(hand_landmarks.landmark):
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
               
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(frame, str(id), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)


            # Check if index finger is raised
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
           
            # Check if pinky finger is raised
            pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            pinky_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
           
            # # Check if middle finger and ring finger are raised
            # middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            # middle_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
            # ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            # ring_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
            # # Check if thumb finger is raised
            # thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            # thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
            if z==0:
              pass
            # Check if only index finger is raised
            if .1+index_finger_tip.y < index_finger_mcp.y and pinky_finger_tip.y >= pinky_finger_pip.y:
                 time.sleep(.2)  # delay to prevent sending too fast
                 print("RIGHT")
                 threading.Thread(target=write_to_serial, args=('r',)).start()

# Check if only pinky finger is raised
            elif index_finger_tip.y >= index_finger_mcp.y and .05+pinky_finger_tip.y < pinky_finger_pip.y:
                time.sleep(.2)  # delay to prevent sending too fast
                print("LEFT")
                threading.Thread(target=write_to_serial, args=('l',)).start()
            elif index_finger_tip.y < index_finger_mcp.y and pinky_finger_tip.y < pinky_finger_pip.y:
                pass
            else:
                pass

            
    # Display frame
    cv2.imshow('Hand Tracking', frame)
    
    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and destroy windows
cap.release()
cv2.destroyAllWindows()