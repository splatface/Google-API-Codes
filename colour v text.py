# this program looks for the dominant colour in an image and checks if the colour of the text is the same as it

from API_folder_name import cv2__library_folder as cv

j_path = r"file for verifying your Google API - .json"
cv.google_auth(j_path)

path = r"image.jpg"

#the colours settings
max = 0
current = 0
actual = (0, 0, 0)

# 0 or 1; checks if same or not
a = 0

p = cv.detect_properties(path)
texts, refPt = cv.detect_text(path)

for i in p.dominant_colors.colors:
    colour = cv.get_colorInfo(i)

    current = colour[1]

    # finds the most apparent colour by comparing new values to the previous ones
    if current > max:
        max = current
        actual = colour[2]

# checks if text colour = text
for t in texts:
    if t.description.upper() == "RED" and actual == (253, 1, 2):
        a = 0
    elif t.description.upper() == "BLUE" and actual == (2, 2, 252):
        a = 0
    elif t.description.upper == "GREEN" and actual == (2, 254, 3):
        a = 0
    else:
        a = 1


# tells user the result
if a == 0:
    print("same", end = ' ')

if a == 1:
    print("different", end = ' ')

if actual[0] >= actual[1] + 70 and actual[0] >= actual[2] + 70:
    print("/ colour similar to red")

if actual[1] >= actual[0] + 70 and actual[1] >= actual[2] + 70:
    print("/ colour similar to blue")

if actual[2] >= actual[1] and actual[2] >= actual[0] + 70:
    print("/ colour similar to green")