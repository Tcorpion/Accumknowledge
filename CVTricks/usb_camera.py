'''
Call the usb camera.

pip install opencv-python==4.4.0.46
'''


import cv2
import numpy as np

cap = cv2.VideoCapture(4)  ##选择第二个摄像头
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
##保存摄像投的数据为视频文件
out = cv2.VideoWriter('camera_test.avi', fourcc, 10.0, size)
while True:
    ret, frame = cap.read()
    # 横向翻转
    frame = cv2.flip(frame, 1)

    frame0 = cv2.equalizeHist(frame[:, :, 0])[:,:,np.newaxis]
    frame1 = cv2.equalizeHist(frame[:, :, 1])[:,:,np.newaxis]
    frame2 = cv2.equalizeHist(frame[:, :, 2])[:,:,np.newaxis]
    out.write(np.concatenate([frame0, frame1, frame2], axis=2))
    # out.write(frame)
    # 在图像上显示 Press Q to save and quit
    cv2.putText(frame,
                "Press Q to save and quit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 0), 2)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()