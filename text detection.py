# finds a stop sign (or any other sign of your choice) in an image

from API_folder_name import cv2__library_folder as cv

j_path = r"file for verifying your Google API - .json"
cv.google_auth(j_path)

path = "image.jpg"
texts,refPt = cv.detect_text(path)
print(refPt)

# cuts down on the path; may not be needed in all situations
q2 = path.find("\\")
k2 = path.find(".")
x = path[q2+1:k2]



p = "image 2.jpg"
text,refPts = cv.detect_text(p)

q = p.find("\\")
k = p.find(".")
v = p[q+1:k]



b = 0
count = 0
c = 0
max = 0
actual = (0,0,0)
m2 = 0
a2 = (0,0,0)

# #all boxed : cv.display_allborders(refPt, path)

# all text extracted
for t in texts:
    print(t.description)

    e = len(texts)

    if e >= 2:
        if t.description.upper() == "STOP":
            cv.display_border(refPt[count], path)
            count = 0
            e -= 1
        count += 1

h = cv.detect_properties(path)

# finds dominant colour
for i in h.dominant_colors.colors:
    colour = cv.get_colorInfo(i)
    print("score:", colour[1]*100, "colour:", colour[2])

    n2 = colour[1]

    if n2 > m2:
        m2 = n2
        a2 = colour[2]

if a2[1] < 77 and a2[0] > 120 and a2[2] < 80:
    print("stop sign detected from", x)
else: 
    print("false alert from", x)

w = len(text)


# finds the word "STOP" within path
for a in text:
    
    if w >= 2:
        if a.description.upper() == "STOP":
            cv.display_border(refPts[c], p)
            c = 0
            w -= 1
        c += 1

r = cv.detect_properties(p)

for i in r.dominant_colors.colors:
    colour = cv.get_colorInfo(i)
    #print("score:", colour[1]*100, "colour:", colour[2])

    now = colour[1]

    if now > max: 
        max = now
        actual = colour[2]

if actual[1] < 77 and actual[0] > 120 and actual[2] < 80:
    print("stop sign detected from", v)
else:
    print("false alert from", v)