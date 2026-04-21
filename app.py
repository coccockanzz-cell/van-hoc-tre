import streamlit as st
import google.generativeai as genai

# ====== CẤU HÌNH TRANG ======
st.set_page_config(
    page_title="Chấm Văn AI",
    page_icon="🌿",
    layout="centered"
)

# ====== CSS CUSTOM ======
st.markdown("""
<style>
body {
    background-color: #f4f9f4;
}

.main {
    background-color: #f4f9f4;
}

h1, h2, h3 {
    color: #2e7d32;
    text-align: center;
}

.stTextInput>div>div>input {
    border-radius: 10px;
}

.stTextArea textarea {
    border-radius: 10px;
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

# ====== HEADER ======
st.title("🌿 Trình Chấm Bài Ngữ Văn AI")
st.caption("✨ Sử dụng Gemini 2.5 Flash - Hỗ trợ giáo viên chấm bài nhanh chóng")

# ====== KIỂM TRA API ======
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Bạn chưa cấu hình API Key trong Streamlit Secrets")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# ====== INPUT ======
with st.container():
    st.subheader("📌 Nhập thông tin bài làm")

    topic = st.text_input(
        "Đề bài",
        placeholder="Ví dụ: Nghị luận về lòng dũng cảm..."
    )

    essay = st.text_area(
        "Bài làm của học sinh",
        height=300,
        placeholder="Dán bài văn vào đây..."
    )

# ====== BUTTON ======
if st.button("🚀 Bắt đầu chấm bài"):
    if not essay.strip():
        st.warning("⚠️ Bạn chưa nhập bài làm")
        st.stop()

    with st.spinner("🤖 AI đang phân tích bài viết..."):
        prompt = f"""
        Bạn là giáo viên Ngữ văn giàu kinh nghiệm.

        Hãy chấm bài văn sau:

        Đề bài: {topic}

        Bài làm:
        {essay}

        Yêu cầu:
        1. Cho điểm (thang 10)
        2. Nhận xét chi tiết (nội dung, diễn đạt, sáng tạo)
        3. Chỉ ra lỗi sai (chính tả, ngữ pháp)
        4. Gợi ý cải thiện cụ thể

        Trình bày rõ ràng, dễ đọc, có tiêu đề từng phần.
        """

        try:
            response = model.generate_content(prompt)

            st.success("✅ Đã chấm xong!")

            st.markdown("### 📊 Kết quả chấm bài")
            st.markdown(
                f"<div class='result-box'>{response.text}</div>",
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"❌ Lỗi: {e}")
            st.info("👉 Nếu lỗi 403: hãy kiểm tra lại API Key")
