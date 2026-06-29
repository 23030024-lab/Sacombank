import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import pymannkendall as mk
import matplotlib.pyplot as plt
import mplfinance as mpf
import sqlite3
import os
import sqlite3

# =============================
# CẤU HÌNH TRANG
# =============================
st.set_page_config(
    page_title="Phân tích cổ phiếu bằng Mann-Kendall",
    page_icon="📈",
    layout="wide"
)

# =============================
# LOGO
# =============================
st.image("logo.jpg")
# =============================
# TIÊU ĐỀ
# =============================
st.title("📈 TRỰC QUAN HÓA GIÁ CỔ PHIẾU VÀ KIỂM ĐỊNH MANN-KENDALL")
st.subheader("HUỲNH THỊ NGỌC TIÊN ĐỀ TÀI 9")

# =============================
# KẾT NỐI SQLITE
# =============================
conn = sqlite3.connect("members.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    bio TEXT
)
""")

conn.commit()
main_col, profile_col = st.columns([4, 1])

with profile_col:

    st.subheader("👥 Thành viên")

    with st.expander("➕ Thêm thành viên"):

        name = st.text_input("Họ tên")
        role = st.text_input("Vai trò")
        bio = st.text_area("Chức vụ")
        color = st.color_picker(
    "Chọn màu hồ sơ",
    "#4CAF50"
)

        if st.button("💾 Lưu hồ sơ"):

            c.execute(
                "INSERT INTO members(name, role, bio) VALUES (?, ?, ?)",
                (name, role, bio)
            )

            conn.commit()

            st.success("Đã lưu thành công!")

    st.markdown("---")

    # =============================
# DATABASE THÀNH VIÊN
# =============================

conn = sqlite3.connect(
    "members.db",
    check_same_thread=False
)

c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS members(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    bio TEXT,
    color TEXT
)
""")

conn.commit()
# =============================
# QUẢN LÝ THÀNH VIÊN
# =============================

st.sidebar.markdown("---")
st.sidebar.header("👥 Thành viên")

with st.sidebar.expander("➕ Thêm thành viên"):

    tv_name = st.text_input("Họ tên")

    tv_role = st.selectbox(
        "Chức vụ",
        [
            "👑 Trưởng nhóm",
            "💻 Lập trình viên",
            "📊 Phân tích dữ liệu",
            "⭐ Thành viên"
        ]
    )

    tv_bio = st.text_area("Tiểu sử")

    tv_color = st.color_picker(
        "Màu hồ sơ",
        "#4CAF50"
    )

    if st.button("💾 Lưu thành viên"):

        if tv_name != "":

            c.execute(
                """
                INSERT INTO members
                (name, role, bio, color)
                VALUES (?, ?, ?, ?)
                """,
                (
                    tv_name,
                    tv_role,
                    tv_bio,
                    tv_color
                )
            )

            conn.commit()

            st.success("Đã lưu!")

            st.rerun()

    # Hiển thị tất cả thành viên
    c.execute("SELECT * FROM members")
    rows = c.fetchall()

       st.subheader("👥 Danh sách thành viên")

cols = st.columns(3)   # 3 hồ sơ trên 1 hàng

for idx, row in enumerate(rows):

    with cols[idx % 3]:

        st.markdown(
            f"""
            <div style="
                background-color:{row[4]};
                padding:15px;
                border-radius:15px;
                text-align:center;
                min-height:250px;
                box-shadow:2px 2px 8px rgba(0,0,0,0.2);
            ">
                <h3>{row[1]}</h3>
                <h4>{row[2]}</h4>
                <p>{row[3]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            f"🗑️ Xóa {row[1]}",
            key=f"delete_{row[0]}"
        ):
            c.execute(
                "DELETE FROM members WHERE id=?",
                (row[0],)
            )

            conn.commit()
            st.rerun()

            st.write("**Vai trò:**", row[2])
            st.write(row[3])

            if st.button(
                f"🗑️ Xóa {row[0]}",
                key=f"delete_{row[0]}"
            ):

                c.execute(
                    "DELETE FROM members WHERE id=?",
                    (row[0],)
                )

                conn.commit()

                st.rerun()
# =============================
# MỤC LỤC TƯƠNG TÁC
# =============================
with st.sidebar:
    st.title("☰ MỤC LỤC")

    menu = st.radio(
        "Chọn nội dung",
        [
            "📋 Thông tin đầu vào",
            "📄 Dữ liệu",
            "📈 Giá đóng cửa và Log Return",
            "🕯️ Biểu đồ nến",
            "📊 Kết quả Mann-Kendall"
        ]
        )
st.markdown("---")
if menu == "📋 Thông tin đầu vào":
    st.markdown(
        "<script>window.location.hash='input';</script>",
        unsafe_allow_html=True
    )

elif menu == "📄 Dữ liệu":
    st.markdown(
        "<script>window.location.hash='data';</script>",
        unsafe_allow_html=True
    )

elif menu == "📈 Giá đóng cửa và Log Return":
    st.markdown(
        "<script>window.location.hash='chart';</script>",
        unsafe_allow_html=True
    )

elif menu == "🕯️ Biểu đồ nến":
    st.markdown(
        "<script>window.location.hash='candle';</script>",
        unsafe_allow_html=True
    )

elif menu == "📊 Kết quả Mann-Kendall":
    st.markdown(
        "<script>window.location.hash='mk';</script>",
        unsafe_allow_html=True
    )

# =============================
# THÔNG TIN ĐẦU VÀO (DẠNG DỌC)
# =============================
st.markdown('<div id="input"></div>', unsafe_allow_html=True)
st.header("📋 Thông tin đầu vào")
# =============================
# DANH SÁCH THÀNH VIÊN
# =============================

st.subheader("👥 Nhóm thực hiện")

c.execute("""
SELECT * FROM members
ORDER BY id
""")

members = c.fetchall()

if members:

    cols = st.columns(3)

    for idx, member in enumerate(members):

        with cols[idx % 3]:

            st.markdown(
                f"""
                <div style="
                    background-color:{member[4]};
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                    min-height:250px;
                    color:white;
                ">
                    <h3>{member[1]}</h3>
                    <h4>{member[2]}</h4>
                    <p>{member[3]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"🗑️ Xóa",
                key=f"del_{member[0]}"
            ):

                c.execute(
                    """
                    DELETE FROM members
                    WHERE id=?
                    """,
                    (member[0],)
                )

                conn.commit()

                st.rerun()

ticker = st.text_input(
    "Mã cổ phiếu",
    value="VCB.VN"
)

start_date = st.date_input(
    "Ngày bắt đầu",
    value=pd.to_datetime("2026-01-01")
)

end_date = st.date_input(
    "Ngày kết thúc",
    value=pd.to_datetime("2026-06-27")
)

run = st.button(
    "📈 Phân tích",
    use_container_width=True
)

# =============================
# CHẠY PHÂN TÍCH
# =============================
if run:

    with st.spinner("Đang tải dữ liệu..."):

        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False
        )

    if df.empty:
        st.error("Không tìm thấy dữ liệu.")
        st.stop()

    # =============================
    # XỬ LÝ DỮ LIỆU
    # =============================
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel("Ticker")

    full_date_range = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq="D"
    )

    df = df.reindex(full_date_range)

    df = df.ffill()

    df["simple_ret"] = df["Close"].pct_change()

    df["log_ret"] = np.log(
        df["Close"] / df["Close"].shift(1)
    )

    # =============================
    # HIỂN THỊ DỮ LIỆU
    # =============================
    st.markdown('<div id="data"></div>', unsafe_allow_html=True)
    st.subheader("📄 Dữ liệu")

    st.dataframe(df)

    # =============================
    # BIỂU ĐỒ GIÁ & LOG RETURN
    # =============================
    st.markdown('<div id="chart"></div>', unsafe_allow_html=True)
    st.subheader("📈 Giá đóng cửa và Log Return")

    fig, ax = plt.subplots(
        2,
        1,
        figsize=(10, 8),
        sharex=True
    )

    ax[0].plot(
        df.index,
        df["Close"],
        color="red",
        linewidth=2,
        label="Close Price"
    )

    ax[0].set_title("Giá đóng cửa")
    ax[0].set_ylabel("VND")
    ax[0].legend()
    ax[0].grid(True)
    ax[1].plot(
        df.index,
        df["log_ret"],
        color="green",
        linewidth=1.5,
        label="Log Return"
    )

    ax[1].set_title("Log Return")
    ax[1].set_ylabel("Return")
    ax[1].set_xlabel("Date")
    ax[1].legend()
    ax[1].grid(True)

    plt.tight_layout()

    st.pyplot(fig)

    # =============================
    # BIỂU ĐỒ NẾN
    # =============================
    st.markdown('<div id="candle"></div>', unsafe_allow_html=True)
    st.subheader("🕯️ Biểu đồ nến")

    fig2, _ = mpf.plot(
        df,
        type="candle",
        mav=(10, 20),
        volume=True,
        style="yahoo",
        figsize=(12, 6),
        title=ticker,
        returnfig=True
    )

    st.pyplot(fig2)

    # =============================
    # KIỂM ĐỊNH MANN-KENDALL
    # =============================
    close_prices = df["Close"].dropna().reset_index(drop=True)

    result = mk.original_test(close_prices)

    st.markdown('<div id="mk"></div>', unsafe_allow_html=True)
    st.subheader("📊 Kết quả kiểm định Mann-Kendall")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Trend", result.trend)
        st.metric("Tau", f"{result.Tau:.4f}")

    with col2:
        st.metric("p-value", f"{result.p:.6f}")
        st.metric("Variance S", f"{result.var_s:.2f}")

    st.markdown("---")

    if result.p < 0.05:
        if result.trend == "increasing":
            st.success("Có xu hướng **TĂNG** có ý nghĩa thống kê (p < 0.05).")
        elif result.trend == "decreasing":
            st.success("Có xu hướng **GIẢM** có ý nghĩa thống kê (p < 0.05).")
        else:
            st.success("Có xu hướng đáng kể về mặt thống kê.")
    else:
        st.warning("Không phát hiện xu hướng có ý nghĩa thống kê (p ≥ 0.05).")
