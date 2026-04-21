import streamlit as st
import google.generativeai as genai
import time

# ====== CONFIG PAGE ======
st.set_page_config(
    page_title="Chấm Văn AI 2.5",
    page_icon="🌿",
    layout="centered"
)

# ====== CUSTOM CSS ======
st.markdown("""
<style>
.main { background-color: #f0f7f0; }
h1 { color: #1b5e20; text-align: center; font-weight: 800; }
.stButton>button {
    background: linear-gradient(90deg, #2e7d32, #1b5e20);
    color: white;
    border-radius: 15px;
    height: 3.5em;
    font-weight: bold;
    width: 100%;
    border: none;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.result-box {
    background-color: white;
    padding: 25px;
    border-radius: 20px;
    border-left: 10px solid #2e7d32;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

st.title("🌿 Trình Chấm Văn AI 2.5")
st.caption("Phiên bản đặc biệt sử dụng Model Gemini 2.5 Flash")

# ====== KẾT NỐI API ======
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Thiếu API Key trong Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Ép hệ thống dùng đúng model 2.5
try:
    model = genai.GenerativeModel("models/gemini-2.5-flash")
except:
    model = genai.GenerativeModel("gemini-2.5-flash")

# ====== QUẢN LÝ THỜI GIAN GỌI API ======
if "last_call" not in st.session_state:
    st.session_state.last_call = 0

# ====== GIAO DIỆN NHẬP LIỆU ======
topic = st.text_input("Đề bài văn", placeholder="Nhập đề bài để AI chấm sát ý hơn...")
essay = st.text_area("Nội dung bài làm", height=350, placeholder="Dán bài văn của học sinh vào đây...")

if st.button("🚀 Bắt đầu chấm với Gemini 2.5"):
    if not essay.strip():
        st.warning("⚠️ Bạn chưa nhập bài văn mà!")
        st.stop()

    # Kiểm tra hạn mức (Rate limit)
    now = time.time()
    if now - st.session_state.last_call < 12:
        st.warning(f"⏳ Hệ thống 2.5 cần nghỉ ngơi một chút. Thử lại sau vài giây nhé!")
        st.stop()

    st.session_state.last_call = now

    prompt = f"""
    Bạn là một giáo viên Ngữ văn cấp cao. Hãy chấm bài văn này thật chuyên nghiệp.
    Đề bài: {topic}
    Bài làm: {essay}
    
    Yêu cầu trả về:
    1. Điểm số cụ thể (thang 10).
    2. Nhận xét ưu điểm nổi bật.
    3. Góp ý về các lỗi diễn đạt, chính tả, bố cục.
    4. Hướng dẫn học sinh cách nâng cao chất lượng bài viết.
    """

    try:
        with st.spinner("🤖 AI 2.5 đang đọc và phân tích bài viết..."):
            response = model.generate_content(prompt)
            
        st.success("✅ Đã hoàn thành!")
        st.markdown("### 📊 Đánh giá từ Giáo viên AI")
        st.markdown(f"<div class='result-box'>{response.text}</div>", unsafe_allow_html=True)
        st.balloons()

    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            st.error("❌ Model 2.5 Flash không khả dụng với API hiện tại. Hãy kiểm tra lại quyền truy cập của Key.")
        elif "429" in error_msg:
            st.error("🚫 Quá hạn mức! Đợi 1 phút rồi nhấn lại Khang nhé.")
        else:
            st.error(f"❌ Lỗi: {error_msg}")
