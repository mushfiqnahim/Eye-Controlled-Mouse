import cv2
import mediapipe as mp
import pyautogui

face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
cam = cv2.VideoCapture(0)

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
                for i in range(474, 478): 
                    landmark = landmarks[i]  # Accessing the landmark correctly
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    if i == 1:  # Using index 1
                        screen_x = screen_w / frame_w * x
                        screen_y = screen_h / frame_h * y
                        pyautogui.moveTo(screen_x, screen_y)
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

                right_eye = [landmarks[145], landmarks[159]]
                right_eye_avg_x = sum([lm.x for lm in right_eye]) / len(right_eye)
                right_eye_avg_y = sum([lm.y for lm in right_eye]) / len(right_eye)

                # Map right-eye movement to screen coordinates
                screen_x = screen_w * right_eye_avg_x
                screen_y = screen_h * right_eye_avg_y
                pyautogui.moveTo(screen_x, screen_y)

                # Draw right eye landmarks
                for lm in right_eye:
                    x = int(lm.x * frame_w)
                    y = int(lm.y * frame_h)
                    cv2.circle(frame, (x, y), 4, (255, 255, 0), -1)
                    print(right_eye[0].y - right_eye[1].y)
                    if (right_eye[0].y - right_eye[1].y) < 0.009:
                      #print('click')
                      pyautogui.click()
                      pyautogui.sleep(1)
        cv2.imshow('Eye Mouse - Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cam.release()
cv2.destroyAllWindows()