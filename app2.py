import streamlit as st
import pytesseract
from PIL import Image
import numpy as np
import cv2
import os

# Ensure TESSDATA_PREFIX is set if needed
tessdata_prefix = os.environ.get('TESSDATA_PREFIX')
if tessdata_prefix:
    os.environ['TESSDATA_PREFIX'] = tessdata_prefix

st.title("Hindi and English Text Extractor")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Load the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert to OpenCV format for processing
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

    # Convert back to PIL Image for Tesseract
    processed_image = Image.fromarray(thresh_image)

    try:
        extracted_text = pytesseract.image_to_string(processed_image, lang='hin+eng')

        st.subheader("Extracted Text:")
        st.text(extracted_text)

        keyword = st.text_input("Enter a keyword to search within the extracted text:")
        
        if keyword:
            if keyword in extracted_text:
                highlighted_text = extracted_text.replace(
                    keyword, f"<span style='color: red; font-weight: bold;'>{keyword}</span>"
                )
                st.subheader("Search Results:")
                st.markdown(highlighted_text.replace("\n", "  \n"), unsafe_allow_html=True)
            else:
                st.write("Keyword not found.")
    except pytesseract.TesseractError as e:
        st.error(f"Tesseract Error: {str(e)}")
        st.error("Please ensure Tesseract is properly installed and configured.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
