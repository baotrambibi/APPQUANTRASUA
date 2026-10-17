import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & CSS TÙY CHỈNH
# ---------------------------------------------------------
st.set_page_config(
    page_title="Bi Coffee & Tea - POS",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #faf9f6;
    }
    .header-banner {
        background: linear-gradient(135deg, #4A2E19 0%, #2E1C0C 100%);
        color: #F4E8C1;
        padding: 1.8rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        margin-bottom: 1.5rem;
    }
    .header-banner h1 {
        color: #E2B963 !important;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .invoice-box {
        background-color: #ffffff;
        border: 2px dashed #4A2E19;
        padding: 20px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DỮ LIỆU SẢN PHẨM & DỊCH VỤ
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

# Khởi tạo session state
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "order_history" not in st.session_state:
    st.session_state.order_history = []

# ---------------------------------------------------------
# 3. SIDEBAR ĐIỀU HƯỚNG
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400", use_container_width=True)
    st.markdown("### ☕ **BI COFFEE & TEA**")
    st.caption("Hệ thống quản lý bán hàng POS")
    st.divider()

    nav_choice = st.radio(
        "📌 Chức năng hệ thống:",
        [
            "🛒 Order Bán Hàng & POS",
            "👨‍🍳 Màn Hình Pha Chế (KDS)",
            "📊 Doanh Thu & Lịch Sử"
        ]
    )

# ---------------------------------------------------------
# 4. CHỨC NĂNG 1: ORDER BÁN HÀNG & POS
# ---------------------------------------------------------
if nav_choice == "🛒 Order Bán Hàng & POS":

    st.markdown("""
        <div class="header-banner">
            <h1>☕ BI COFFEE & TEA 🌿</h1>
            <p>"Thưởng thức
