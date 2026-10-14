import streamlit as st

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 ỨNG DỤNG TÍNH LÃI GỬI TIẾT KIỆM")
st.write("Tính lãi theo phương pháp lãi đơn và lãi kép")


# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_money(value):
    return f"{value:,.0f} VNĐ"


# ==============================
# NHẬP DỮ LIỆU
# ==============================
st.subheader("📌 Thông tin tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1
)

hinh_thuc_lai = st.selectbox(
    "Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_lanh = st.selectbox(
    "Hình thức lãnh lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)


# ==============================
# NÚT TÍNH TOÁN
# ==============================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if ky_han <= 0:
        st.error("Kỳ hạn phải lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được âm.")
        st.stop()

    # Chuyển đổi
    lai_nam = lai_suat / 100
    so_nam = ky_han / 12

    # ==============================
    # TÍNH LÃI ĐƠN
    # ==============================
    if hinh_thuc_lai == "Lãi đơn":

        tong_tien_lai = so_tien * lai_nam * so_nam
        tong_goc_lai = so_tien + tong_tien_lai

        # Lãi định kỳ
        if hinh_thuc_lanh == "Lãnh lãi theo tháng":
            lai_dinh_ky = so_tien * lai_nam / 12

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":
            lai_dinh_ky = so_tien * lai_nam / 4

        else:
            lai_dinh_ky = tong_tien_lai

    # ==============================
    # TÍNH LÃI KÉP
    # ==============================
    else:

        if hinh_thuc_lanh == "Lãnh lãi theo tháng":
            # Ghép lãi hàng tháng
            so_ky = ky_han
            lai_ky = lai_nam / 12

            tong_goc_lai = so_tien * (1 + lai_ky) ** so_ky
            tong_tien_lai = tong_goc_lai - so_tien

            # Lãi của kỳ đầu tiên
            lai_dinh_ky = so_tien * lai_ky

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":
            # Ghép lãi hàng quý
            so_ky = ky_han / 3
            lai_ky = lai_nam / 4
          tong_goc_lai = so_tien * (1 + lai_ky) ** so_ky
            tong_tien_lai = tong_goc_lai - so_tien

            # Lãi của quý đầu tiên
            lai_dinh_ky = so_tien * lai_ky

        else:
            # Lãnh lãi cuối kỳ
            # Ghép lãi theo năm
            so_ky = so_nam

            tong_goc_lai = so_tien * (1 + lai_nam) ** so_ky
            tong_tien_lai = tong_goc_lai - so_tien

            lai_dinh_ky = tong_tien_lai

    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================
    st.divider()
    st.subheader("📊 KẾT QUẢ TÍNH TOÁN")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_tien_lai)
        )

    with col3:
        st.metric(
            "💰 Tổng gốc + lãi",
            format_money(tong_goc_lai)
        )

    # ==============================
    # THÔNG TIN CHI TIẾT
    # ==============================
    st.divider()

    st.write("### 📝 Thông tin khoản tiền gửi")

    st.write(f"**Số tiền gửi:** {format_money(so_tien)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Phương pháp:** {hinh_thuc_lai}")
    st.write(f"**Hình thức lãnh lãi:** {hinh_thuc_lanh}")

    st.success(
        f"🎉 Sau {ky_han} tháng, tổng số tiền bạn nhận được là "
        f"**{format_money(tong_goc_lai)}**."
    )
