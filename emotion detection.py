from API_folder_name import cv2__library_folder as cv

j_path = r"file for verifying your Google API - .json"
cv.google_auth(j_path)

path = r"image.jpg"
faces, refPt = cv.detect_faces(path, max_results = 200) # detects a maximum of ___ (here 200) faces in the image

emotions, face_box = cv.display_emotion(faces)
likelyname = ("UNKHNOWN", "VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY")

c = 0

for f in faces:
    for e in emotions:
        anger, joy, surp, sor = e
        
        # finds how likely it is for each person to be the following:
        print("anger: {}", likelyname[anger])
        print("joy: {}", likelyname[joy])
        print("surprise: {}", likelyname[surp])
        print("sad: {}", likelyname[sor])

        c += 1

        if joy != "UNKNOWN" or joy != "VERY UNLIKELY" or joy != "UNLIKELY":
            cv.display_border(refPt[c], path) # makes a border around the face