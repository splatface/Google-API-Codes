from API_folder_name import cv2__library_folder as cv
import cv2

max = 0
actual = (0, 0, 0)

cv.google_auth(r"file for verifying your Google API - .json")

#path = r"Term 6\stop sign.jpg"
path = r"image.jpg"
p = cv.detect_properties(path)

for i in p.dominant_colors.colors:
    colour = cv.get_colorInfo(i)
    print("pixel fraction:", colour[0], "score:", colour[1]*100, "RGB:", colour[2]) # this is the meaning of the values in cv.get.colorInfo(i)
    print(colour[1])

    now = colour[1]
    
    if now > max:
        max = now
        actual = colour[2]
    
print("max:", max*100)
print("actual:", actual)

actual2 = (actual[2], actual[1], actual[0])
#cv.make_bar(500, 500, [actual2])

if actual[1] > 200:
    print("yield sign")
else:
    print("stop sign")