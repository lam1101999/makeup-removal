import facenet_pytorch
import numpy as np
class FaceDetector():
    def __init__(self):
        self.mtcnn = facenet_pytorch.MTCNN()
        
    def detect_face(self, image, resized=False, size=96):
        images = []
        boxes, _ = self.mtcnn.detect(image)
        for box in boxes:
            box = np.clip(box, 0, min(image.height, image.width))
            left, top, right, bottom = box
            face_image = image.crop((left, top, right, bottom))
            if resized:
                face_image = face_image.resize((size, size))
            images.append(face_image)
        return images