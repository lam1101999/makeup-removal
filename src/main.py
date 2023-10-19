import streamlit as st
from FaceDetector import FaceDetector
from MakeupRemover import MakeupRemover
from PIL import Image
import numpy as np
import torch
import pathlib
import os


def main():
    face_detector = FaceDetector()
    makeup_remover = MakeupRemover()
    st.title("WebApp Makeup Remove")
    st.header("A Project in AI class")
    image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if image_file is not None:
        our_image = Image.open(image_file)
        st.text("Original Image:")
        st.image(our_image, channels="RGB")
        faces = face_detector.detect_face(our_image, resized=True, size=96)
        
        for face in faces:
            remove_makeup = makeup_remover.remove_makeup(face["image"])
            print(remove_makeup)
            restored_size = Image.fromarray((remove_makeup*255).astype(np.uint8)).resize((face["width"], face["height"]))
            information = "After removing makeup"
            st.text(information)
            st.image(restored_size, channels="RGB")


if __name__ == "__main__":
    main()