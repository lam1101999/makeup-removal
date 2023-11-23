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
    image_file = st.file_uploader(
        "Upload an image", type=["png", "jpg", "jpeg"])
    if image_file is not None:
        our_image = Image.open(image_file).convert("RGB")
        st.markdown("Your input image:")
        st.image(our_image, channels="RGB")
        faces = face_detector.detect_face(our_image)
        information = f"**Detect {len(faces)} faces:**"
        st.markdown(information)

        for index, face in enumerate(faces):
            # Remove makeup
            remove_makeup = makeup_remover.remove_makeup(face["image"])
            remove_makeup = Image.fromarray(
                (remove_makeup*255).astype(np.uint8)).resize((face["width"], face["height"]))

            # Display result
            col1, col2, col3 = st.columns(3, gap="small")
            col1.text(f"face {index + 1}:")
            col2.image(face["image"],
                       width=face["image"].width, channels="RGB")
            col3.image(remove_makeup, width=remove_makeup.width,
                       channels="RGB")


if __name__ == "__main__":
    main()
