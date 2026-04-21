import streamlit as st
import google.generativeai as genai
import time

# ====== CONFIG PAGE ======
st.set_page_config(
    page_title="Chấm Văn AI",
    page_icon="🌿",
    layout="centered"
)

# ====== CUSTOM CSS ======
st.markdown("""
<style>
body {
    background-color: #f4f9f4;
}

h1, h2, h3 {
    color: #2e7d32;
    text-align: center;
}

.stButton>button {
    background: linear-gradient(90deg, #2e7d32, #66bb6a);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
    width: 100%;
    border: none;
}

.result-box {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border-left: 6px solid #2e7d32;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ====== TITLE ======
st.title("🌿 Trình Chấm Bài Ngữ Văn AI")
st.caption("Sử dụng Gemini AI hỗ trợ giáo viên chấm bài")

# ====== CHECK API KEY ======
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Chưa cấu hình GEMINI_API_KEY trong Streamlit Secrets")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 👉 đổi model để ổn định hơn
model = genai.GenerativeModel("gemini-1.5-flash")

# ====== SESSION STATE (chống spam) ======
if "last_call" not in st.session_state:
    st.session_state.last_call = 0

# ====== INPUT UI ======
st.subheader("📌 Nhập bài làm")

topic = st.text_input("Đề bài", placeholder="Ví dụ: Nghị luận về lòng dũng cảm...")
essay = st.text_area("Bài làm", height=300, placeholder="Dán bài văn vào đây...")

# ====== BUTTON ======
if st.button("🚀 Chấm bài ngay"):

    if not essay.strip():
        st.warning("⚠️ Vui lòng nhập bài làm")
        st.stop()

    now = time.time()

    # ====== CHỐNG SPAM ======
    if now - st.session_state.last_call < 10:
        wait_time = int(10 - (now - st.session_state.last_call))
        st.warning(f"⏳ Vui lòng đợi {wait_time}s trước khi chấm tiếp")
        st.stop()

    st.session_state.last_call = now

    # ====== PROMPT ======
    prompt = f"""
    Bạn là giáo viên Ngữ văn giàu kinh nghiệm.

    Đề bài: {topic}

    Bài làm:
    {essay}

    Yêu cầu:
    1. Chấm điểm (thang 10)
    2. Nhận xét chi tiết
    3. Chỉ lỗi chính tả / diễn đạt
    4. Gợi ý cải thiện
    """

    try:
        with st.spinner("🤖 AI đang chấm bài..."):
            time.sleep(2)  # giảm spam API
            response = model.generate_content(prompt)

        st.success("✅ Chấm bài hoàn tất!")

        st.markdown("### 📊 Kết quả")
        st.markdown(f"<div class='result-box'>{response.text}</div>", unsafe_allow_html=True)

    except Exception as e:
        if "429" in str(e):
            st.error("🚫 Bạn gửi quá nhiều request. Vui lòng đợi 1 phút rồi thử lại.")
        else:
            st.error(f"❌ Lỗi hệ thống: {e}")
