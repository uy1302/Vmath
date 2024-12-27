import streamlit as st
from together import Together
import pytesseract
from PIL import Image
import os

# Cài đặt API key của Together
os.environ['TOGETHER_API_KEY'] = 'cb763da0569fe7e125dabfb7d4d31eacb0fc80f5f4cca4f3e4c6d62dca5b081c'
api_key = os.environ.get('TOGETHER_API_KEY')

# Khởi tạo client của Together
client = Together(api_key=api_key)

# Cài đặt đường dẫn cho Tesseract (tuỳ thuộc vào hệ điều hành)
# Đối với Windows, bạn cần chỉ định đường dẫn Tesseract cài đặt.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Ứng dụng Streamlit
st.title("VMathbot - Hệ thống hỗ trợ giải đáp câu hỏi Toán học")
st.write("Nhập câu hỏi của bạn dưới dạng văn bản hoặc tải lên một hình ảnh!")

# Người dùng chọn kiểu nhập liệu
input_type = st.radio("Chọn kiểu nhập liệu:", ["Văn bản", "Hình ảnh"])

if input_type == "Văn bản":
    # Nhập câu hỏi từ người dùng
    user_input = st.text_input("Câu hỏi Toán học của bạn:")
    
    if st.button("Gửi"):
        if not user_input.strip():
            st.warning("Vui lòng nhập câu hỏi.")
        else:
            with st.spinner("Đang xử lý..."):
                messages = [{"role": "user", "content": user_input}]
                response = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                    messages=messages,
                    max_tokens=None,
                    temperature=0.7,
                    top_p=0.7,
                    top_k=50,
                    repetition_penalty=1,
                    stop=["<|eot_id|>", "<|eom_id|>"],
                    stream=True
                )

                # Xử lý và hiển thị kết quả
                bot_response = ""
                for token in response:
                    if hasattr(token, 'choices'):
                        delta_content = token.choices[0].delta.content
                        bot_response += delta_content

                st.success("Câu trả lời từ VMathbot:")
                st.text(bot_response)

elif input_type == "Hình ảnh":
    # Tải lên hình ảnh
    uploaded_file = st.file_uploader("Tải lên hình ảnh chứa câu hỏi:", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Hình ảnh đã tải lên", use_container_width=True)

        # Trích xuất văn bản từ hình ảnh
        with st.spinner("Đang trích xuất văn bản từ hình ảnh..."):
            extracted_text = pytesseract.image_to_string(image, lang="vie+math")  # Hỗ trợ cả tiếng Việt và tiếng Anh

        st.write("Nội dung trích xuất:")
        
        # Cho phép người dùng chỉnh sửa văn bản trích xuất
        edited_text = st.text_area("Chỉnh sửa văn bản nếu cần thiết:", extracted_text, height=200)

        if st.button("Gửi câu hỏi từ hình ảnh"):
            if not edited_text.strip():
                st.warning("Không thể trích xuất nội dung từ hình ảnh. Vui lòng thử lại.")
            else:
                with st.spinner("Đang xử lý..."):
                    messages = [{"role": "user", "content": edited_text}]
                    response = client.chat.completions.create(
                        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                        messages=messages,
                        max_tokens=None,
                        temperature=0.7,
                        top_p=0.7,
                        top_k=50,
                        repetition_penalty=1,
                        stop=["<|eot_id|>", "<|eom_id|>"],
                        stream=True
                    )

                    # Xử lý và hiển thị kết quả
                    bot_response = ""
                    for token in response:
                        if hasattr(token, 'choices'):
                            delta_content = token.choices[0].delta.content
                            bot_response += delta_content

                    st.success("Câu trả lời từ VMathbot:")
                    st.text(bot_response)
