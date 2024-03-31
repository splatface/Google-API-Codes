# this program detects faces from 2+ different images

from API_folder_name import cv2__library_folder as cv

j_path = r"file for verifying your Google API - .json"
cv.google_auth(j_path)

path1 = r"image.jpg" 
path2 = r"image2.jpg"
paths = [path1, path2]

# cv.display_allborders(refPt, path)

for p in paths:
    faces, refPt = cv.detect_faces(p, max_results = 200)

    for face in faces:
        #left eye coordinates
        x1 = int(face.landmarks[17].position.x)
        y1 = int(face.landmarks[17].position.y)

        x2 = int(face.landmarks[18].position.x)
        y2 = int(face.landmarks[18].position.y)

        x3 = int(face.landmarks[19].position.x)
        y3 = int(face.landmarks[19].position.y)

        x4 = int(face.landmarks[16].position.x)
        y4 = int(face.landmarks[16].position.y)

        point = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

        cv.display_border(point, p) # shows a border at "point" on "p"

        #right eye coordinates
        x1_2 = int(face.landmarks[22].position.x)
        y1_2 = int(face.landmarks[22].position.y)

        x2_2 = int(face.landmarks[24].position.x)
        y2_2 = int(face.landmarks[24].position.y)

        x3_2 = int(face.landmarks[23].position.x)
        y3_2 = int(face.landmarks[23].position.y)

        x4_2 = int(face.landmarks[25].position.x)
        y4_2 = int(face.landmarks[25].position.y)

        point2 = [(x1_2, y1_2), (x2_2, y2_2), (x3_2, y3_2), (x4_2, y4_2)]

        cv.display_border(point2, p)