import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Bi Coffee & Tea - POS System",
    page_icon="☕",
    layout="wide"
)

# ---------------------------------------------------------
# 2. MENU SẢN PHẨM & DỊCH VỤ
# ---------------------------------------------------------
MENU_ITEMS = {
    "☕ CÀ PHÊ": {
        "Cà Phê Đen Đá": {
            "price": 25000, 
            "img": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500"
        },
        "Cà Phê Sữa Đá": {
            "price": 28000, 
            "img": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500"
        },
        "Bạc Xỉu": {
            "price": 32000, 
            "img": "https://images.unsplash.com/photo-1541167760496-1628856ab772?w=500"
        },
        "Matcha Espresso Latte": {
            "price": 42000, 
            "img": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=500"
        }
    },
    "🧋 TRÀ & TRÀ SỮA": {
        "Matcha Latte": {
            "price": 40000, 
            "img": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=500"
        },
        "Trà Sữa Trân Châu Đường Đen": {
            "price": 35000, 
            "img": "https://images.unsplash.com/photo-1558857563-b371033873b8?w=500"
        },
        "Trà Sữa Thái Xanh": {
            "price": 32000, 
            "img": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=500"
        },
        "Trà Đào Cam Sả": {
            "price": 35000, 
            "img": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=500"
        },
        "Trà Dâu Tằm": {
            "price": 32000, 
            "img": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500"
        }
    },
    "🍰 BÁNH & NGỌT": {
        "Bánh Croissant Bơ Tỏi": {
            "price": 29000,
            "img": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=500"
        },
        "Bánh Tiramisu": {
            "price": 35000,
            "img": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=500"
        }
    }
}

SIZE_OPTIONS = {
    "S (Vừa)": 0,
    "M (Lớn)": 5000,
    "L (Đặc biệt)": 10000
}

TOPPING_OPTIONS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000
}

SUGAR_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0% (Không đường)"]
ICE_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0% (Không đá)"]

# Khởi tạo lưu trữ trạng thái đơn hàng
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "order_history" not in st.session_state:
    st.session_state.order_history = []

# ---------------------------------------------------------
# 3. THANH MENU BÊN TRÁI (SIDEBAR)
# ---------------------------------------------------------
with st.sidebar:
    st.title("☕ BI COFFEE & TEA")
    st.caption("Hệ thống POS Quản Lý Bán Hàng")
    st.divider()

    nav_choice = st.radio(
        "Chức năng:",
        [
            "🛒 Order Bán Hàng",
            "👨‍🍳 Màn Hình Pha Chế",
            "📊 Doanh Thu & Lịch Sử"
        ]
    )

# ---------------------------------------------------------
# 4. CHỨC NĂNG 1: ORDER BÁN HÀNG
# ---------------------------------------------------------
if nav_choice == "🛒 Order Bán Hàng":

    st.title("☕ BI COFFEE & TEA 🌿")
    st.caption("Thưởng thức hương vị Trà Sữa & Cà Phê thơm ngon")
    st.divider()

    col_left, col_right = st.columns([1.2, 0.8])

    # ================= CỘT TRÁI: CHỌN MÓN =================
    with col_left:
        st.subheader("📝 Thông tin đơn hàng")
        
        c_name, c_tier, c_type = st.columns([2, 1.2, 1])
        with c_name:
            customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên khách...")
        with c_tier:
            cust_tier = st.selectbox("Thành viên:", ["Khách vãng lai", "VIP (-10%)", "HSSV (-5%)"])
        with c_type:
            service_type = st.selectbox("Hình thức:", ["Tại bàn", "Mang đi"])

        st.subheader("🍵 Chọn món nước & Tùy chọn")

        # Chọn nhóm sản phẩm
        selected_category = st.radio(
            "Danh mục món:", 
            list(MENU_ITEMS.keys()), 
            horizontal=True
        )

        category_dict = MENU_ITEMS[selected_category]

        c_select, c_preview = st.columns([1.2, 1])

        with c_select:
            # Chọn món
            selected_item_name = st.selectbox("Tên món:", list(category_dict.keys()))
            item_info = category_dict[selected_item_name]
            base_price = item_info["price"]

            quantity = st.number_input("Số lượng:", min_value=1, value=1, step=1)

            # Chọn Size, Đường, Đá
            c_sz, c_sg, c_ic = st.columns(3)
            with c_sz:
                selected_size = st.selectbox("Size:", list(SIZE_OPTIONS.keys()))
            with c_sg:
                selected_sugar = st.selectbox("Đường:", SUGAR_LEVELS)
            with c_ic:
                selected_ice = st.selectbox("Đá:", ICE_LEVELS)

            selected_toppings = st.multiselect("Topping:", options=list(TOPPING_OPTIONS.keys()))

        # HIỂN THỊ HÌNH TỰ ĐỘNG
        with c_preview:
            st.write("**Hình minh họa:**")
            st
