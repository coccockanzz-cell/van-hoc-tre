import streamlit as st
from openai import OpenAI

# ====== CONFIG PAGE ======
st.set_page_config(
    page_title="Chấm Văn AI (ChatGPT)",
    page_icon="🌿",
    layout="centered"
)

# ====== GIAO DIỆN XANH LÁ ======
st.markdown("""
<style>
.main { background-color: #f0f7f0; }
h1 { color: #10a37f; text-align: center; font-weight: 800; } /* Màu xanh đặc trưng OpenAI */
.stButton>button {
    background: linear-gradient(90deg, #10a37f, #058567);
    color: white;
    border-radius: 15px;
    height: 3.5em;
    font-weight: bold;
    width: 100%;
    border: none;
}
.result-box {
    background-color: white;
    padding: 25px;
    border-radius: 20px;
    border-left: 10px solid #10a37f;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

st.title("🌿 Trình Chấm Văn AI (ChatGPT)")
st.caption("Sử dụng công nghệ GPT-4o từ OpenAI để chấm bài Ngữ văn")

# ====== KẾT NỐI API OPENAI ======
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ Thiếu mã OPENAI_API_KEY trong phần Secrets của Streamlit!")
    st.stop()

# Khởi tạo client OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ====== GIAO DIỆN NHẬP LIỆU ======
topic = st.text_input("Đề bài văn", placeholder="Nhập đề bài...")
essay = st.text_area("Nội dung bài làm", height=350, placeholder="Dán bài văn vào đây...")

if st.button("🚀 Bắt đầu chấm bài ngay"):
    if not essay.strip():
        st.warning("⚠️ Bạn chưa nhập nội dung bài làm.")
        st.stop()

    try:
        with st.spinner("🤖 ChatGPT đang đọc và chấm bài..."):
            # Gọi model GPT-4o
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Bạn là một giáo viên Ngữ văn chuyên nghiệp."},
                    {"role": "user", "content": f"Chấm điểm bài văn sau.\nĐề bài: {topic}\nNội dung: {essay}\n\nYêu cầu: Trả về điểm số/10, nhận xét ưu nhược điểm và hướng dẫn cải thiện."}
                ],
                temperature=0.7
            )
            
        st.success("✅ Đã hoàn thành!")
        st.markdown("### 📊 Kết quả từ ChatGPT")
        st.markdown(f"<div class='result-box'>{response.choices[0].message.content}</div>", unsafe_allow_html=True)
        st.balloons()

    except Exception as e:
        if "insufficient_quota" in str(e):
            st.error("❌ Tài khoản OpenAI của bạn hết tiền hoặc hết hạn mức. Hãy nạp tiền (min 5$) nhé!")
        else:
            st.error(f"❌ Lỗi: {e}")
