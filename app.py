import streamlit as st
from openai import OpenAI

# 1. Cấu hình trang
st.set_page_config(
    page_title="Chấm Văn AI - ChatGPT",
    page_icon="🌿",
    layout="centered"
)

# 2. Giao diện CSS
st.markdown("""
<style>
    .main { background-color: #f7f9f7; }
    h1 { color: #10a37f; text-align: center; font-family: 'Segoe UI', sans-serif; }
    .stButton>button {
        background: linear-gradient(90deg, #10a37f, #058567);
        color: white;
        border-radius: 12px;
        height: 3.5em;
        font-weight: bold;
        width: 100%;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(16, 163, 127, 0.3); }
    .result-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #10a37f;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

st.title("🌿 Trình Chấm Văn AI (ChatGPT)")
st.caption("Ứng dụng hỗ trợ giảng dạy Ngữ văn - Sử dụng GPT-4o")

# 3. Kết nối API
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ Chưa tìm thấy mã OPENAI_API_KEY trong Secrets!")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 4. Giao diện nhập liệu
topic = st.text_input("Đề bài văn", placeholder="Nhập đề bài tại đây...")
essay = st.text_area("Bài làm của học sinh", height=350, placeholder="Dán bài văn vào đây...")

if st.button("🚀 Bắt đầu chấm bài"):
    if not essay.strip():
        st.warning("⚠️ Vui lòng nhập nội dung bài làm!")
    else:
        try:
            with st.spinner("🤖 ChatGPT đang phân tích bài viết..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Bạn là giáo viên Ngữ văn giỏi. Hãy chấm bài văn chi tiết: Điểm (thang 10), Ưu điểm, Nhược điểm, và Gợi ý sửa lỗi."},
                        {"role": "user", "content": f"Đề bài: {topic}\n\nBài làm: {essay}"}
                    ],
                    temperature=0.7
                )
                
            st.success("✅ Đã chấm xong!")
            st.markdown("### 📊 Kết quả đánh giá")
            st.markdown(f"<div class='result-box'>{response.choices[0].message.content}</div>", unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            if "insufficient_quota" in str(e):
                st.error("❌ Tài khoản OpenAI hết hạn mức hoặc hết tiền. Khang kiểm tra lại nhé!")
            else:
                st.error(f"❌ Lỗi hệ thống: {e}")
