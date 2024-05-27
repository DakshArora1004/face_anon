import cv2
import mediapipe as mp
import argparse
def process_img(img,face_detection):
    img_rgb=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results=face_detection.process(img_rgb)
    if results.detections is not None:
        for detection in results.detections:
            x1=detection.location_data.relative_bounding_box.xmin
            y1=detection.location_data.relative_bounding_box.ymin
            x2=detection.location_data.relative_bounding_box.xmin+detection.location_data.relative_bounding_box.width
            y2=detection.location_data.relative_bounding_box.ymin+detection.location_data.relative_bounding_box.height
            x1=int(x1*W)
            y1=int(y1*H)
            x2=int(x2*W)
            y2=int(y2*H)
            #blur face
            img[y1:y2, x1:x2]=cv2.blur(img[y1:y2,x1:x2],(100,100))
    return img        

args=argparse.ArgumentParser()
args.add_argument("--mode" , default="webcam")
args.add_argument("--filePath", default = "man.jpg")
args=args.parse_args()
#read image



#detect face
mp_face_detect=mp.solutions.face_detection
with mp_face_detect.FaceDetection(min_detection_confidence=0.5, model_selection =0) as face_detection:
    if args.mode in ["image"]:
        img=cv2.imread(args.filePath)
        H,W,_=img.shape
        img=process_img(img,face_detection)
    elif args.mode in ["webcam"]:
        cap=cv2.VideoCapture(0)
        while True:
            ret, img=cap.read()
            H,W,_=img.shape
            img=process_img(img,face_detection)
            cv2.imshow("image",img)
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()




#save image