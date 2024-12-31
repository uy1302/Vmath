import streamlit as st
import google.generativeai as genai
import pytesseract
from PIL import Image
import os

# Set the Google Gemini API key directly as an environment variable
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAzTO35qULvghLRJLC9K_HZZfYOQImFwO4'  # Replace with your API key

# Initialize the Google Gemini client with API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Streamlit app
st.title("VMathbot - Hệ thống hỗ trợ giải đáp câu hỏi Toán học")
st.write("Nhập câu hỏi của bạn dưới dạng văn bản hoặc tải lên một hình ảnh!")

# User selects input type
input_type = st.radio("Chọn kiểu nhập liệu:", ["Văn bản", "Hình ảnh"])

if input_type == "Văn bản":
    # Input math question from the user
    user_input = st.text_input("Câu hỏi Toán học của bạn:")
    
    if st.button("Gửi"):
        if not user_input.strip():
            st.warning("Vui lòng nhập câu hỏi.")
        else:
            with st.spinner("Đang xử lý..."):
                model = genai.GenerativeModel("gemini-1.5-pro")  # Get the Gemini 1.5 Pro model
                response = model.generate_content(
                    user_input
                )

                # Display the result
                st.success("Câu trả lời từ VMathbot:")
                st.text(response.text)

elif input_type == "Hình ảnh":
    # Upload image
    uploaded_file = st.file_uploader("Tải lên hình ảnh chứa câu hỏi:", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Hình ảnh đã tải lên", use_container_width=True)

        # Extract text from the image
        with st.spinner("Đang trích xuất văn bản từ hình ảnh..."):
            extracted_text = pytesseract.image_to_string(image, lang="vie+math")  # Supports both Vietnamese and Math

        st.write("Nội dung trích xuất:")
        
        # Allow the user to edit the extracted text
        edited_text = st.text_area("Chỉnh sửa văn bản nếu cần thiết:", extracted_text, height=200)

        if st.button("Gửi câu hỏi từ hình ảnh"):
            if not edited_text.strip():
                st.warning("Không thể trích xuất nội dung từ hình ảnh. Vui lòng thử lại.")
            else:
                with st.spinner("Đang xử lý..."):
                    model = genai.GenerativeModel("gemini-1.5-pro")
                    response = model.generate_content(
                        edited_text
                    )

                    # Display the result
                    st.success("Câu trả lời từ VMathbot:")
                    st.text(response.text)
