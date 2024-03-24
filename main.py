import cv2
import mediapipe as mp
import time

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
           
            # Check if middle finger and ring finger are raised
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
            # Check if thumb finger is raised
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
        # Check if only index finger is raised
            elif .1+index_finger_tip.y < index_finger_mcp.y and .2+pinky_finger_tip.y >= pinky_finger_pip.y:
                time.sleep(.2)
                print("RIGHT")

        # Check if only pinky finger is raised
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
    # Display frame
    cv2.imshow('Hand Tracking', frame)
    
    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and destroy windows
cap.release()
cv2.destroyAllWindows()