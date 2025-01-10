######################################### eye track with mouse control ##############################################
import cv2
import mediapipe as mp
import pyautogui
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
cam = cv2.VideoCapture(0)
pyautogui.FAILSAFE = False 

if not cam.isOpened():
    print("Error: Cannot access the camera.")
else:
    print("Press 'q' to quit.")

    while True:
        ret, frame = cam.read() 
        frame = cv2.flip(frame, 1)

        if not ret:
            print("Error: Frame capture failed.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            for face_landmarks in landmark_points:
                landmarks = face_landmarks.landmark

                right_eye_index = [362, 263, 373, 374, 380] 

                # Calculate the average x, y of the right eye landmarks for better accuracy
                right_eye_x, right_eye_y = 0, 0
                for idx in right_eye_index:
                    right_eye_x += landmarks[idx].x
                    right_eye_y += landmarks[idx].y
                right_eye_x /= len(right_eye_index)
                right_eye_y /= len(right_eye_index)

                # Calculate the position of the cursor based on the right eye position
                # Normalize the coordinates to the screen size
                screen_x = int(right_eye_x * screen_w)
                screen_y = int(right_eye_y * screen_h)
                pyautogui.moveTo(screen_x, screen_y)
                right_eye = (int(right_eye_x * frame_w), int(right_eye_y * frame_h))
                cv2.circle(frame, right_eye, 3, (0, 255, 0), -1)

       
        cv2.imshow('Eye Mouse - Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cam.release()
cv2.destroyAllWindows()