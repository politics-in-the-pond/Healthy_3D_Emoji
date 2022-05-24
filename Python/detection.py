import sys
import cv2
import mediapipe
from math import sqrt

COUNTER = 0
TOTAL_BLINKS = 0

FONT = cv2.FONT_HERSHEY_SIMPLEX

# landmarks from mesh_map.jpg
LEFT_EYE = [ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
RIGHT_EYE = [ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]

mediapipe_face_mesh = mediapipe.solutions.face_mesh
face_mesh = mediapipe_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence =0.6, min_tracking_confidence=0.7)

video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def landmarksDetection(image, results, draw=False):
    image_height, image_width= image.shape[:2]
    mesh_coordinates = [(int(point.x * image_width), int(point.y * image_height)) for point in results.multi_face_landmarks[0].landmark]
    if draw :
        [cv2.circle(image, i, 2, (0, 255, 0), -1) for i in mesh_coordinates]
    return mesh_coordinates

# Euclaidean distance to calculate the distance between the two points
def euclaideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = sqrt((x1 - x)**2 + (y1 - y)**2)
    return int(distance)

# Blinking Ratio
def blinkRatio(landmarks, right_indices, left_indices):

    right_eye_landmark1 = landmarks[right_indices[0]]
    right_eye_landmark2 = landmarks[right_indices[8]]

    right_eye_landmark3 = landmarks[right_indices[12]]
    right_eye_landmark4 = landmarks[right_indices[4]]

    left_eye_landmark1 = landmarks[left_indices[0]]
    left_eye_landmark2 = landmarks[left_indices[8]]

    left_eye_landmark3 = landmarks[left_indices[12]]
    left_eye_landmark4 = landmarks[left_indices[4]]

    right_eye_horizontal_distance = euclaideanDistance(right_eye_landmark1, right_eye_landmark2)
    right_eye_vertical_distance = euclaideanDistance(right_eye_landmark3, right_eye_landmark4)

    left_eye_vertical_distance = euclaideanDistance(left_eye_landmark3, left_eye_landmark4)
    left_eye_horizobtal_distance = euclaideanDistance(left_eye_landmark1, left_eye_landmark2)

    right_eye_ratio = right_eye_horizontal_distance/right_eye_vertical_distance
    left_eye_ratio = left_eye_horizobtal_distance/left_eye_vertical_distance

    eyes_ratio = (right_eye_ratio+left_eye_ratio)/2

    return eyes_ratio


while True:
    ret, frame = video_capture.read()
    frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
    frame = cv2.flip(frame,1)
    frame_height, frame_width= frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    results  = face_mesh.process(rgb_frame)
    
    if results.multi_face_landmarks:
        coord = landmarksDetection(frame, results, True)

        eyes_ratio = blinkRatio(coord, RIGHT_EYE, LEFT_EYE)

        if eyes_ratio > 3.3:
            COUNTER +=1

        else:
            if COUNTER > 3:
                TOTAL_BLINKS +=1
                COUNTER =0
        cv2.putText(frame, f'Total Blinks: {TOTAL_BLINKS}',(10, 20), FONT, 1, (0, 255, 0), 2)

        # Send Data
        posX = coord[356][0]
        posY = coord[168][1]
        sizeHead = int((euclaideanDistance(coord[192],coord[282]) + euclaideanDistance(coord[52],coord[416])) / 2)
        roll = (coord[145][1] - coord[374][1])
        yaw = euclaideanDistance(coord[195],coord[130]) - euclaideanDistance(coord[195],coord[359])
        pitch = int(((coord[145][1] - coord[5][1]) + ( coord[374][1] - coord[5][1] )) / 2)

        # send to Unity
        print("FromPython", posX, posY, sizeHead, roll, yaw, pitch)
        sys.stdout.flush()

    cv2.imshow('Liveness Detection', frame)
    if cv2.waitKey(2) == 27:
        break
        
cv2.destroyAllWindows()
video_capture.release()


#Position
# index[6].x, y 미간
# 범위_ x: 0 ~ 640, y: 0 ~ 480

#Head scale 
# (([152].y - [10].y) + ([447].x - [227].x)) / 2
# ((coord[152][1] - coord[10][1]) + (coord[447][0] - coord[227][0])) / 2
# 범위_ 70 ~ 370


#Turn
# roll  (z턴)       눈의 y 값 차이
#                   [145].y - [374].y
# 범위_ x: -100 ~ 100

# yaw   (좌우)      코와 눈 거리 차이
#                   euclid([195], [130]) - euclid([359], [195])
# 범위_ x: -55 ~ 55

# pitch (위아래)    코와 눈 y 값 차이
#                   ([145].y - [5].y) + ([374]y - [5].y)
# (mesh_coordinatess[5][1] - mesh_coordinatess[145][1]) + (mesh_coordinatess[5][1] - mesh_coordinatess[374][1])) / 2
# 범위_ x: 0 ~ 50


