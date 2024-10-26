from ultralytics import YOLO

class Detector:
    def __init__(self, weights='weights/face.pt'):
        self.model = YOLO(model=weights, task='detection')

    def detect(self, image, min_conf=0.5, max_iou=0.7, min_area=0.1):
        image_h, image_w, _ = image.shape
        results = self.model.predict(image, verbose=False, conf=min_conf, iou=max_iou)[0].boxes.data.cpu().numpy().tolist()
        bboxes = []
        for xmin, ymin, xmax, ymax, conf, _ in results:
            if ((xmax - xmin) * (ymax - ymin)) / (image_h * image_w) > min_area:
                bboxes.append([xmin, ymin, xmax, ymax, conf])
        return bboxes

if __name__ == '__main__':
    import cv2 as cv
    model = Detector()
    camera = cv.VideoCapture(0)
    while camera.isOpened():
        ret, frame = camera.read()
        if not ret:
            break
        bboxes = model.detect(frame)
        for xmin, ymin, xmax, ymax, conf in bboxes:
            frame = cv.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
            frame = cv.putText(frame, f'{conf}', (int(xmin), int(ymin - 20)), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
        cv.imshow('Frame', frame)
        if cv.waitKey(1) == 27:
            break
    camera.release()
