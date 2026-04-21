import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện
st.set_page_config(page_title="Chấm Văn AI 2.5", page_icon="🌿")

st.markdown("<h1 style='color: #2e7d32;'>🌿 Hệ thống Chấm Văn Sư Phạm</h1>", unsafe_allow_html=True)

# Lấy API Key từ Secrets (Bảo mật)
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Chưa cài đặt API Key trong Secrets!")
    else:
        # Cấu hình Gemini
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Gọi chính xác model 2.5 Flash
        model = genai.GenerativeModel('gemini-2.5-flash')

        topic = st.text_input("Đề bài:")
        essay = st.text_area("Bài làm của học sinh:", height=300)

        if st.button("🚀 Bắt đầu chấm bài"):
            if essay:
                with st.spinner("AI 2.5 đang phân tích..."):
                    prompt = f"Bạn là giáo viên Ngữ văn. Chấm bài văn này: {essay} theo đề: {topic}. Trả về điểm và nhận xét chi tiết."
                    response = model.generate_content(prompt)
                    st.success("Đã chấm xong!")
                    st.info(response.text)
            else:
                st.warning("Hãy dán bài văn vào nhé!")
except Exception as e:
    st.error(f"Lỗi: {e}")
