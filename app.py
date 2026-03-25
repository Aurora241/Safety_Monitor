import streamlit as st
import cv2
import pandas as pd
from ultralytics import YOLO
from datetime import datetime
import time

# ── Cấu hình trang ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Giám sát An toàn Lao động",
    page_icon="🦺",
    layout="wide"
)

st.title("Hệ thống Giám sát An toàn Lao động")
st.markdown("Phát hiện mũ bảo hộ & áo phản quang theo thời gian thực")
st.divider()

# ── Load model ───────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return YOLO("best_20260320_0316.pt")

model = load_model()
CLASS_NAMES  = model.names
VIOLATIONS = ['head', 'person']

# ── Sidebar cấu hình ─────────────────────────────────────────────────
with st.sidebar:
    st.header("Cấu hình")

    camera_option = st.radio(
        "Nguồn camera",
        ["Webcam máy tính", "IP Webcam (điện thoại)"]
    )

    if camera_option == "IP Webcam (điện thoại)":
        ip_url = st.text_input(
            "Địa chỉ IP Webcam",
            value="http://192.168.1.x:8080/video",
            help="Xem địa chỉ IP trên app IP Webcam của điện thoại"
        )
        source = ip_url
    else:
        source = 0

    conf = st.slider("Ngưỡng confidence", 0.1, 0.9, 0.5, 0.05)
    st.divider()

    if st.button("Xóa lịch sử", use_container_width=True):
        st.session_state.violations = []
        st.rerun()

    st.divider()
    st.markdown("**Chú thích:**")
    st.markdown("🟢 hardhat / vest = Tuân thủ")
    st.markdown("🔴 no-hardhat / no-vest = Vi phạm")

# ── Session state ────────────────────────────────────────────────────
if "violations" not in st.session_state:
    st.session_state.violations = []

# ── Layout ───────────────────────────────────────────────────────────
col_video, col_log = st.columns([2, 1])

with col_video:
    st.subheader("Live Camera")
    frame_display = st.empty()

with col_log:
    st.subheader("🔔 Trạng thái")
    status_display = st.empty()

    st.subheader("📊 Thống kê")
    metric_display = st.empty()

    st.subheader("📋 Vi phạm gần nhất")
    log_display = st.empty()

# ── Bắt đầu giám sát ────────────────────────────────────────────────
run = st.toggle("▶️ Bắt đầu giám sát", value=False)

if run:
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        st.error("❌ Không mở được camera! Kiểm tra lại kết nối.")
        st.stop()

    total   = 0
    vio_cnt = 0

    while run:
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ Mất kết nối camera!")
            break

        # Detect
        results   = model(frame, conf=conf, verbose=False)[0]
        annotated = results.plot(line_width=2)
        total    += 1

        # Kiểm tra vi phạm
        found_violations = []
        for box in results.boxes:
            cls = CLASS_NAMES[int(box.cls)]
            if cls in VIOLATIONS:
                found_violations.append(cls)

        ts = datetime.now().strftime("%H:%M:%S")

        if found_violations:
            vio_cnt += 1
            for v in found_violations:
                st.session_state.violations.append({
                    "Thời gian" : ts,
                    "Vi phạm"   : v,
                    "Confidence": f"{float(results.boxes[0].conf):.2f}"
                })
            status_display.error(f"❌ VI PHẠM: {', '.join(found_violations)}\n\n⏰ {ts}")
        else:
            status_display.success(f"✅ Tuân thủ quy định\n\n⏰ {ts}")

        # Hiển thị frame
        frame_display.image(
            cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
            use_container_width=True
        )

        # Thống kê
        rate = vio_cnt / max(total, 1) * 100
        metric_display.markdown(f"""
| Chỉ số | Giá trị |
|--------|---------|
| Tổng frames | {total} |
| Frames vi phạm | {vio_cnt} |
| Tỷ lệ vi phạm | {rate:.1f}% |
""")

        # Log vi phạm
        if st.session_state.violations:
            df = pd.DataFrame(st.session_state.violations[-8:]).iloc[::-1]
            log_display.dataframe(df, use_container_width=True, hide_index=True)

        time.sleep(0.03)

    cap.release()

else:
    frame_display.info("👆 Bật toggle để bắt đầu giám sát")

# ── Lịch sử đầy đủ + xuất CSV ───────────────────────────────────────
st.divider()
st.subheader("📜 Toàn bộ lịch sử vi phạm")

if st.session_state.violations:
    df_full = pd.DataFrame(st.session_state.violations)
    st.dataframe(df_full, use_container_width=True, hide_index=True)

    csv = df_full.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="⬇️ Xuất báo cáo CSV",
        data=csv,
        file_name=f"violations_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )
else:
    st.info("Chưa có vi phạm nào được ghi nhận.")