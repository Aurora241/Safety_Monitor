# 🦺 Hệ thống Giám sát An toàn Lao động

Hệ thống tự động phát hiện vi phạm trang bị bảo hộ lao động (PPE) tại công trường sử dụng **YOLOv8** và **Streamlit**.

---

## 📋 Tính năng

- 🎥 Nhận diện realtime qua **webcam máy tính**, **IP Webcam WiFi** hoặc **DroidCam USB**
- 🔍 Phát hiện 4 trạng thái: `hardhat` · `vest` · `no-hardhat` · `no-vest`
- 🚨 Cảnh báo tức thì khi phát hiện vi phạm
- 📊 Thống kê tỷ lệ vi phạm theo thời gian thực
- 📋 Lưu lịch sử vi phạm và xuất báo cáo CSV

---

## 🗂️ Cấu trúc thư mục

```
safety_monitor/
├── app.py        ← Web dashboard Streamlit
├── best_20260320_0316.pt       ← Model YOLOv8 đã huấn luyện
└── README.md
```

---

## ⚙️ Yêu cầu hệ thống

- Python 3.10 hoặc 3.11
- Windows / macOS / Linux
- RAM tối thiểu 4GB
- Camera (webcam / điện thoại)

---

## 🚀 Cài đặt

**Bước 1 — Clone hoặc tải project về máy**

Tạo thư mục `safety_monitor/` và đặt `app.py` + `best_20260320_0316.pt` vào trong.

**Bước 2 — Cài thư viện**

Mở terminal (hoặc terminal trong VS Code) tại thư mục project:

```bash
pip install streamlit ultralytics opencv-python pandas
```

---

## ▶️ Chạy ứng dụng

```bash
streamlit run app.py
```

Trình duyệt tự động mở tại `http://localhost:8501`

---

## 📱 Kết nối camera điện thoại

Có 2 cách kết nối camera điện thoại Android:

### Cách 1 — IP Webcam qua WiFi

> Điện thoại và máy tính phải cùng mạng WiFi

1. Tải app **IP Webcam** trên CH Play
2. Mở app → kéo xuống → nhấn **Start server**
3. Màn hình điện thoại hiện địa chỉ IP kiểu `http://192.168.x.x:8080`
4. Trong Streamlit: chọn **IP Webcam (điện thoại)** → nhập địa chỉ `http://192.168.x.x:8080/video`

### Cách 2 — DroidCam qua USB (ổn định hơn)

1. Tải app **DroidCam** trên CH Play
2. Tải **DroidCam Client** trên máy tính tại `dev47apps.com`
3. Bật **USB Debugging** trên điện thoại:
   - Cài đặt → Giới thiệu về điện thoại → nhấn **Số bản dựng 7 lần**
   - Cài đặt → Tùy chọn nhà phát triển → bật **USB Debugging**
4. Cắm dây USB → mở DroidCam trên cả 2 thiết bị → chọn **USB** → Connect
5. Trong Streamlit: chọn **Webcam máy tính** (DroidCam USB = camera 0)

---

## 🖥️ Hướng dẫn sử dụng

### Giao diện chính

```
┌─────────────────────────────┬──────────────────┐
│                             │  🔔 Trạng thái   │
│      📹 Live Camera         │  📊 Thống kê     │
│      (Video realtime)       │  📋 Vi phạm      │
│                             │     gần nhất     │
└─────────────────────────────┴──────────────────┘
│  ▶️ Toggle Bắt đầu giám sát                    │
└─────────────────────────────────────────────────┘
│  📜 Toàn bộ lịch sử vi phạm                    │
│  ⬇️ Xuất báo cáo CSV                           │
└─────────────────────────────────────────────────┘
```

### Các bước sử dụng

1. **Chọn nguồn camera** trong sidebar (trái màn hình)
2. **Điều chỉnh ngưỡng Confidence** (mặc định 0.5)
   - Tăng lên nếu hay cảnh báo nhầm
   - Giảm xuống nếu hay bỏ sót vi phạm
3. **Bật toggle** "▶️ Bắt đầu giám sát"
4. Hệ thống tự động phát hiện và cảnh báo
5. Nhấn **⬇️ Xuất báo cáo CSV** để lưu lịch sử vi phạm

---

## 🏷️ Nhãn phát hiện

| Nhãn | Màu khung | Ý nghĩa | Hành động |
|------|-----------|---------|-----------|
| `hardhat` | Xanh dương | Đang đội mũ bảo hộ | ✅ Tuân thủ |
| `vest` | Xanh lá | Đang mặc áo phản quang | ✅ Tuân thủ |
| `no-hardhat` | Đỏ | Không đội mũ bảo hộ | ❌ Cảnh báo |
| `no-vest` | Cam | Không mặc áo phản quang | ❌ Cảnh báo |

---

## ⚠️ Xử lý lỗi thường gặp

**Không mở được camera:**
```
❌ Không mở được camera! Kiểm tra lại kết nối.
```
→ Kiểm tra địa chỉ IP đã thêm `/video` chưa: `http://192.168.x.x:8080/video`  
→ Đảm bảo điện thoại và máy tính cùng mạng WiFi  
→ Thử đổi số camera: `0`, `1`, `2`

**App chạy chậm / giật:**  
→ Giảm độ phân giải trong app IP Webcam xuống 640x480  
→ Đóng các ứng dụng khác đang chạy

**Không tìm thấy best.pt:**
```
FileNotFoundError: best.pt not found
```
→ Đảm bảo file `best.pt` nằm cùng thư mục với `app.py`

---

## 📊 Thông tin mô hình

| Thông số | Giá trị |
|---------|---------|
| Kiến trúc | YOLOv8s |
| Dataset | HardHat-Vest Dataset v3 |
| Số ảnh train | ~2.600 ảnh |
| Epochs | 50 |
| Image size | 416×416 |
| mAP@50 | ~87.4% |
| Precision | ~87.5% |
| Recall | ~82.4% |

---

## 🛠️ Công nghệ sử dụng

| Thư viện | Phiên bản | Mục đích |
|---------|----------|---------|
| `ultralytics` | 8.x | YOLOv8 inference |
| `streamlit` | 1.x | Web dashboard |
| `opencv-python` | 4.x | Xử lý video/camera |
| `pandas` | 2.x | Xử lý dữ liệu |
| `torch` | 2.x | Deep learning backend |

---

## 📁 Output

Khi xuất báo cáo, file CSV được lưu với định dạng:

```
violations_YYYYMMDD_HHMM.csv
```

Nội dung gồm các cột: `Thời gian`, `Vi phạm`, `Confidence`

---

*Dataset: [HardHat-Vest Dataset v3](https://www.kaggle.com/datasets/muhammetzahitaydn/hardhat-vest-dataset-v3) — Kaggle*
