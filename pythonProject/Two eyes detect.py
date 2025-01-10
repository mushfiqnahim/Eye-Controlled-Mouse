###################################### two eye detect ######################################  
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
                    landmark = landmarks[i]  
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    if i == 1:  
                        screen_x = screen_w / frame_w * x
                        screen_y = screen_h / frame_h * y
                        pyautogui.moveTo(screen_x, screen_y)
                        right_eye = [landmarks[474], landmarks[478]]
                        right_eye_avg_x = sum([lm.x for lm in right_eye]) / len(right_eye)
                        right_eye_avg_y = sum([lm.y for lm in right_eye]) / len(right_eye)
                        screen_x = screen_w * right_eye_avg_x
                        screen_y = screen_h * right_eye_avg_y
                        pyautogui.moveTo(screen_x, screen_y)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

                left_eye_landmarks = [landmarks[145], landmarks[159]]  
                for landmark in left_eye_landmarks:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (255, 255, 0), -1)
                print(left_eye_landmarks[0].y - left_eye_landmarks[1].y)
                if (left_eye_landmarks[0].y - left_eye_landmarks[1].y) < 0.00789:
                    print ('click')
                    pyautogui.click()
                    # pyautogui.sleep(1)
        cv2.imshow('Eye Mouse - Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()