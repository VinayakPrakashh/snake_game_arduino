import cv2
import mediapipe as mp
import time

# Initialize hand tracking module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open video capture
cap = cv2.VideoCapture(0)

while True:
 
    ret, frame = cap.read()
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(frame_rgb)
    
 
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, landmark in enumerate(hand_landmarks.landmark):
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
               
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(frame, str(id), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)


       
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
           
         
            pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            pinky_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
           
       
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
          
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]

            if thumb_tip.y > thumb_mcp.y:
                
                print("START")
                time.sleep(1)
            elif (thumb_tip.y > thumb_mcp.y and
                middle_finger_tip.y < middle_finger_pip.y and
                ring_finger_tip.y < ring_finger_pip.y and
                index_finger_tip.y < index_finger_mcp.y and
                pinky_finger_tip.y < pinky_finger_pip.y ):
                pass
            elif middle_finger_tip.y < middle_finger_pip.y and ring_finger_tip.y < ring_finger_pip.y:
                
                print("STOP")
                time.sleep(1)
        
            elif .1+index_finger_tip.y < index_finger_mcp.y and .2+pinky_finger_tip.y >= pinky_finger_pip.y:
                time.sleep(.2)
                print("RIGHT")

     
            elif 5+index_finger_tip.y >= index_finger_mcp.y and .08+pinky_finger_tip.y < pinky_finger_pip.y:
                time.sleep(.2)
                print("LEFT")
            if (thumb_tip.y > thumb_mcp.y and
                middle_finger_tip.y < middle_finger_pip.y and
                ring_finger_tip.y < ring_finger_pip.y and
                index_finger_tip.y < index_finger_mcp.y and
                pinky_finger_tip.y < pinky_finger_pip.y ):
                pass
            else:
                time.sleep(.2)
                pass
    
    cv2.imshow('Hand Tracking', frame)
    
  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()