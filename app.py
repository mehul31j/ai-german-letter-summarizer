import streamlit as st
from ocr_utils import extract_text_from_image
from summarizer import summarize_text, extract_key_points

st.title("🇩🇪 AI German Letter & Contract Summarizer")

uploaded_file = st.file_uploader("Upload a letter (image/pdf)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Document", use_column_width=True)
    german_text = extract_text_from_image(uploaded_file)
    st.subheader("📄 Extracted German Text")
    st.text(german_text)

    if st.button("🧠 Summarize & Extract Key Points"):
        summary = summarize_text(german_text)
        key_points = extract_key_points(german_text)

        st.subheader("📝 Summary")
        st.write(summary)
        st.subheader("📌 Key Points")
        for point in key_points:
            st.markdown(f"- {point}")
