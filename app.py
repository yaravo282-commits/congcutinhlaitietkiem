import streamlit as st

# ==========================================
# 1. CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==========================================
# 2. GIAO DIỆN
# ==========================================
st.title("💰 TÍNH LÃI GỬI TIẾT KIỆM")
st.write(
    "Ứng dụng giúp bạn tính toán tiền lãi và tổng số tiền "
    "nhận được theo phương pháp lãi đơn hoặc lãi kép."
)

st.divider()


# ==========================================
# 3. HÀM ĐỊNH DẠNG TIỀN
# ==========================================
def format_money(value):
    return f"{value:,.0f} VNĐ"


# ==========================================
# 4. NHẬP THÔNG TIN TIỀN GỬI
# ==========================================
st.subheader("📌 THÔNG TIN TIỀN GỬI")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0,
    value=10_000_000,
    step=1_000_000,
    format="%d"
)

ky_han = st.number_input(
    "Kỳ hạn gửi (tháng)",
    min_value=1,
    max_value=1200,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc_lai = st.selectbox(
    "Phương pháp tính lãi",
    ["Lãi đơn", "Lãi kép"]
)

hinh_thuc_lanh = st.selectbox(
    "Hình thức lãnh lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.caption(
    "Lưu ý: Đây là công cụ mô phỏng tính lãi theo công thức toán học, "
    "không thay thế bảng tính lãi chính thức của ngân hàng."
)


# ==========================================
# 5. TÍNH TOÁN VÀ HIỂN THỊ KẾT QUẢ
# ==========================================
if st.button("🧮 TÍNH LÃI NGAY", use_container_width=True):

    # Kiểm tra dữ liệu
    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")

    else:
        # Chuyển đổi dữ liệu
        tien_gui = float(so_tien)
        so_thang = int(ky_han)
        lai_nam = lai_suat / 100
        so_nam = so_thang / 12

        # --------------------------------------
        # TRƯỜNG HỢP 1: LÃI ĐƠN
        # --------------------------------------
        if hinh_thuc_lai == "Lãi đơn":

            tong_tien_lai = tien_gui * lai_nam * so_nam
            tong_goc_lai = tien_gui + tong_tien_lai

            if hinh_thuc_lanh == "Lãnh lãi theo tháng":
                lai_dinh_ky = tien_gui * lai_nam / 12

            elif hinh_thuc_lanh == "Lãnh lãi theo quý":
                lai_dinh_ky = tien_gui * lai_nam / 4

            else:
                lai_dinh_ky = tong_tien_lai

        # --------------------------------------
        # TRƯỜNG HỢP 2: LÃI KÉP
        # --------------------------------------
        else:

            if hinh_thuc_lanh == "Lãnh lãi theo tháng":
                # Ghép lãi hàng tháng
                tong_goc_lai = tien_gui * (
                    1 + lai_nam / 12
                ) ** so_thang

                lai_dinh_ky = tien_gui * lai_nam / 12

            elif hinh_thuc_lanh == "Lãnh lãi theo quý":
                # Ghép lãi theo quý đầy đủ.
                # Phần tháng lẻ được tính theo lãi suất tháng.
                so_quy = so_thang // 3
                thang_le = so_thang % 3

                tien_sau_quy = tien_gui * (
                    1 + lai_nam / 4
                ) ** so_quy

                tong_goc_lai = tien_sau_quy * (
                    1 + lai_nam / 12
                ) ** thang_le

                lai_dinh_ky = tien_gui * lai_nam / 4

            else:
                # Mô phỏng ghép lãi hàng năm
                tong_goc_lai = tien_gui * (
                    1 + lai_nam
                ) ** so_nam

                lai_dinh_ky = tong_goc_lai - tien_gui

            tong_tien_lai = tong_goc_lai - tien_gui

        # --------------------------------------
        # HIỂN THỊ KẾT QUẢ
        # --------------------------------------
        st.divider()
        st.subheader("📊 KẾT QUẢ TÍNH TOÁN")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="💵 Tiền lãi định kỳ",
                value=format_money(lai_dinh_ky)
            )

        with col2:
            st.metric(
                label="📈 Tổng tiền lãi",
                value=format_money(tong_tien_lai)
            )

        with col3:
            st.metric(
                label="💰 Tổng gốc + lãi",
                value=format_money(tong_goc_lai)
            )

        # --------------------------------------
        # CHI TIẾT KHOẢN TIỀN GỬI
        # --------------------------------------
        st.divider()
        st.subheader("📝 CHI TIẾT KHOẢN TIỀN GỬI")

        st.write(f"**Số tiền gửi:** {format_money(tien_gui)}")
        st.write(f"**Kỳ hạn:** {so_thang} tháng")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
        st.write(f"**Phương pháp tính lãi:** {hinh_thuc_lai}")
        st.write(f"**Hình thức lãnh lãi:** {hinh_thuc_lanh}")

        st.success(
            f"Sau {so_thang} tháng, tổng số tiền gốc và lãi "
            f"theo mô hình tính toán là "
            f"{format_money(tong_goc_lai)}."
        )

        # --------------------------------------
        # GIẢI THÍCH CÔNG THỨC
        # --------------------------------------
        with st.expander("📚 Xem công thức tính lãi"):

            if hinh_thuc_lai == "Lãi đơn":
                st.write(
                    "**Công thức lãi đơn:**\n\n"
                    "Tiền lãi = Tiền gốc × Lãi suất năm × Số năm\n\n"
                    "Tổng tiền = Tiền gốc + Tiền lãi"
                )

            else:
                st.write(
                    "**Công thức lãi kép:**\n\n"
                    "Tổng tiền = Tiền gốc × (1 + lãi suất mỗi kỳ) "
                    "** số kỳ\n\n"
                    "Tiền lãi = Tổng tiền − Tiền gốc"
                )

        st.caption(
            "Kết quả chỉ mang tính tham khảo. Lãi suất thực tế, "
            "cách ghép lãi, ngày gửi và quy định của từng ngân hàng "
            "có thể làm thay đổi số tiền nhận được."
        )
