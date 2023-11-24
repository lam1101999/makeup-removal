import streamlit as st
from FaceDetector import FaceDetector
from MakeupRemover import MakeupRemover
from Classifier import Classifier
from PIL import Image
import numpy as np


def main():

    # Init models
    face_detector = FaceDetector()
    makeup_remover = MakeupRemover()
    classifier = Classifier()
    classifier.choose_model("resnet34")

    # Decorate main page
    st.title("WebApp Makeup Remove")
    st.header("A Project in AI class")
    
    # Sidebar
    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0
    image_list = st.sidebar.file_uploader(
        "Upload an image", type=["png", "jpg", "jpeg"], accept_multiple_files= True, key=st.session_state["file_uploader_key"])
    if st.sidebar.button('Reset'):
        st.session_state["file_uploader_key"] += 1
        st.experimental_rerun()

    # Sidebar to select model
    @st.cache_data
    def load_model(model_name):
        classifier.choose_model(model_name)
    model_list = ["resnet34", "mobile_net_v3_large"]
    model_name = st.sidebar.selectbox(
        "Model name", model_list)
    load_model(model_name)

    # Process input image
    if image_list is not None:
        for image in image_list:
            st.markdown("--------------------------------------------------------")
            our_image = Image.open(image).convert("RGB")
            st.markdown("Your input image:")
            st.image(our_image, channels="RGB")
            faces = face_detector.detect_face(our_image)
            information = f"**Detect {len(faces)} faces:**"
            st.markdown(information)

            for index, face in enumerate(faces):
                # Remove makeup
                predict_class, proba = classifier.predict(face["image"])
                if predict_class[0] == 1:
                    info = "makeup detected"
                    remove_makeup = makeup_remover.remove_makeup(face["image"])
                    remove_makeup = Image.fromarray(
                        (remove_makeup*255).astype(np.uint8)).resize((face["width"], face["height"]))
                else:
                    info = "No makeup detected."
                    remove_makeup = face["image"]

                # Display result
                col1, col2, col3 = st.columns(3, gap="medium")
                col1.text(f"face {index + 1}:")
                col2.image(face["image"], caption="Original",
                        width=face["image"].width, use_column_width="auto", channels="RGB")
                col3.image(remove_makeup, caption=info, width=remove_makeup.width, use_column_width="auto",
                        channels="RGB")

if __name__ == "__main__":
    main()
