import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & CSS TÙY CHỈNH (GIAO DIỆN HIỆN ĐẠI)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Bi Coffee & Tea - POS System",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện sang trọng, hiện đại
st.markdown("""
<style>
    /* Tổng thể nền và font */
    .main {
        background-color: #faf9f6;
    }
    
    /* Custom Banner Header */
    .header-banner {
        background: linear-gradient(135deg, #4A2E19 0%, #2E1C0C 100%);
        color: #F4E8C1;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        margin-bottom: 2rem;
    }
    .header-banner h1 {
        color: #E2B963 !important;
        font-family: 'Trebuchet MS', sans-serif;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .header-banner p {
        font-style: italic;
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Thẻ hiển thị món hàng (Card) */
    .product-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* Custom nút bấm */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Biển hiệu hoá đơn */
    .invoice-container {
        background-color: #ffffff;
        border: 2px dashed #4A2E19;
        padding: 20px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DỮ LIỆU SẢN PHẨM & DỊCH VỤ (KÈM HÌNH ẢNH DEMO)
# ---------------------------------------------------------
# Danh mục món: Bao gồm giá và link ảnh online minh họa
MENU_ITEMS = {
    "CÀ PHÊ": {
        "Cà Phê Đen Đá": {
            "price": 25000, 
            "img": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500"
        },
        "Cà Phê Sữa Đá": {
            "price": 28000, 
            "img": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500"
        },
        "Bac Xiu Hot/Ice": {
            "price": 32000, 
            "img": "https://images.unsplash.com/photo-1541167760496-1628856ab772?w=500"
        },
        "Matcha Espresso Latte": {
            "price": 42000, 
            "img": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=500"
        }
    },
    "TRÀ & TRÀ SỮA": {
        "Matcha Latte Premium": {
            "price": 40000, 
            "img": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=500"
        },
        "Trà Sữa Trân Châu Đường Đen": {
            "price": 35000, 
            "img": "
