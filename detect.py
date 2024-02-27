from datetime import datetime
import cv2, pandas

df = pandas.DataFrame(columns = ["Entry Time", "Exit Time", "Entry(for Plot)", "Exit(for Plot)"])
times = []
s_list = [None, None]
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ff = None
while True:
    c, f = video.read()
    s = "No Object"
    f_g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    f_g = cv2.GaussianBlur(f_g, (17, 17), 0)

    if ff is None:
        ff = f_g
        continue

    del_frame = cv2.absdiff(ff, f_g)
    threshold_frame = cv2.threshold(del_frame, 40, 255, cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame, None, iterations= 2)

    (cont, _) = cv2.findContours(threshold_frame.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in cont:
        if cv2.contourArea(c) < 10000:
            continue
        s = "Object Detected"
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(f, (x, y), (x+w, y+h), (0,0,255), 3)
    s_list.append(s)

    if s_list[-1] == "Object Detected" and s_list[-2] == "No Object":
        times.append(datetime.now())
    if s_list[-1] == "No Object" and s_list[-2] == "Object Detected":
        times.append(datetime.now())


    # cv2.imshow("Grey", f_g)
    # cv2.imshow("Delta", del_frame)
    # cv2.imshow("Threshold", threshold_frame)
    cv2.imshow("Rectangle", f)

    if cv2.waitKey(1) == ord("q"):
        if s == "Object":
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    df = df.append({"Entry Time": times[i].strftime("%d-%m -> %H:%M:%S"), "Exit Time": times[i + 1].strftime("%d-%m -> %H:%M:%S"), "Entry(for Plot)": times[i], "Exit(for Plot)": times[i + 1]}, ignore_index = True)

df.index.name = "S.No"
df.index += 1
df.to_csv("times.csv")

video.release()
cv2.destroyAllWindows