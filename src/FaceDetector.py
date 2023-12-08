import facenet_pytorch
import numpy as np
class FaceDetector():
    def __init__(self):
        self.mtcnn = facenet_pytorch.MTCNN()
        
    def detect_face(self, image, resized=False, size=(96, 96)):
        faces_data = []
        boxes, _ = self.mtcnn.detect(image)
        boxes = boxes if boxes is not None else []
        for box in boxes:
            box = np.clip(box, 0, max(image.height, image.width))
            left, top, right, bottom = box
            face_image = image.crop((left, top, right, bottom))
            element_data = dict()
            if resized:
                element_data["image"] = face_image.resize(size)
            else:
                element_data["image"] = face_image
            element_data["width"] = face_image.width
            element_data["height"] = face_image.height
            faces_data.append(element_data)
        return faces_data
