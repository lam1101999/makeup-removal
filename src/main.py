import streamlit as st
from FaceDetector import FaceDetector
from MakeupRemover import MakeupRemover
from PIL import Image
import numpy as np


def main():
    face_detector = FaceDetector()
    makeup_remover = MakeupRemover()
    st.title("WebApp Makeup Remove")
    st.header("A Project in AI class")
    image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if image_file is not None:
        our_image = Image.open(image_file).convert("RGB")
        st.text("Original Image:")
        st.image(our_image, channels="RGB")
        faces = face_detector.detect_face(our_image, resized=True, size=96)
        
        information = f"Detect {len(faces)} faces:"
        st.text(information)
        for index,face in enumerate(faces):
            st.text(f"face {index + 1}:")
            remove_makeup = makeup_remover.remove_makeup(face["image"])
            restored_size = Image.fromarray((remove_makeup*255).astype(np.uint8)).resize((face["width"], face["height"]))
            st.image(restored_size, channels="RGB")


if __name__ == "__main__":
    main()