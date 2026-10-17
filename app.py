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
# 2. MENU SẢN PHẨM KÈM LINK ẢNH TRỰC TUYẾN
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
# HÀM XUẤT HÓA ĐƠN DẠNG TEXT (.TXT)
# ---------------------------------------------------------
def create_txt_invoice(customer_name, service_type, cart, total_amount, discount, final_amount):
    """Tạo nội dung văn bản cho file hóa đơn TXT"""
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    content = f"{'='*40}\n"
    content += f"{'HÓA ĐƠN BÁN HÀNG - BI COFFEE & TEA':^40}\n"
    content += f"{'='*40}\n"
    content += f"Ngày: {now}\n"
    content += f"Khách hàng: {customer_name if customer_name else 'Khách vãng lai'}\n"
    content += f"Hình thức: {service_type}\n"
    content += f"{'-'*40}\n"
    
    for idx, item in enumerate(cart, 1):
        content += f"{idx}. {item['Tên món']}"
        if item['Size'] != "-":
            content += f" ({item['Size']})"
        content += f"\n"
        if item['Đường'] != "-":
            content += f"   - Đường: {item['Đường']} | Đá: {item['Đá']}\n"
        if item['Topping'] != "Không":
            content += f"   - Topping: {item['Topping']}\n"
        content += f"   SL: {item['Số lượng']} x {item['Đơn giá']:,} = {item['Thành tiền']:,} VNĐ\n"
        
    content += f"{'-'*40}\n"
    content += f"Tổng tiền món: {total_amount:,} VNĐ\n"
    content += f"Giảm giá: {discount}%\n"
    content += f"TỔNG THANH TOÁN: {final_amount:,} VNĐ\n"
    content += f"{'='*40}\n"
    content += f"{'Cảm ơn quý khách và hẹn gặp lại!':^40}\n"
    return content

# ---------------------------------------------------------
# 3. SIDEBAR ĐIỀU HƯỚNG
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
# 4. CHỨC NĂNG 1: ORDER BÁN HÀNG & POS
# ---------------------------------------------------------
if nav_choice == "🛒 Order Bán Hàng":

    st.title("☕ BI COFFEE & TEA 🌿")
    st.caption("Hệ thống tính tiền và gọi món nhanh chóng")
    st.divider()

    col_left, col_right = st.columns([1.2, 0.8])

    # ==================== CỘT TRÁI: CHỌN MÓN ====================
    with col_left:
        st.subheader("📝 Thông tin đơn hàng")
        
        c_name, c_tier, c_type = st.columns([2, 1.2, 1])
        with c_name:
            customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên khách...")
        with c_tier:
            cust_tier = st.selectbox("Thành viên:", ["Khách vãng lai", "VIP (-10%)", "HSSV (-5%)"])
        with c_type:
            service_type = st.selectbox("Hình thức:", ["Tại bàn", "Mang đi"])

        st.subheader("🍵 Chọn sản phẩm & Tùy chọn")

        selected_category = st.radio(
            "Danh mục món:", 
            list(MENU_ITEMS.keys()), 
            horizontal=True
        )

        category_dict = MENU_ITEMS[selected_category]

        # Chia 2 cột: Cột chọn chi tiết món & Cột xem hình ảnh minh họa
        c_select, c_preview = st.columns([1.2, 1])

        with c_select:
            selected_item_name = st.selectbox("Tên món:", list(category_dict.keys()))
            item_info = category_dict[selected_item_name]
            base_price = item_info["price"]

            quantity = st.number_input("Số lượng:", min_value=1, value=1, step=1)

            # KIỂM TRA: NẾU KHÔNG PHẢI LÀ BÁNH NGỌT THÌ HIỆN SIZE, ĐƯỜNG, ĐÁ, TOPPING
            if "BÁNH" not in selected_category:
                c_sz, c_sg, c_ic = st.columns(3)
                with c_sz:
                    selected_size = st.selectbox("Size:", list(SIZE_OPTIONS.keys()))
                with c_sg:
                    selected_sugar = st.selectbox("Đường:", SUGAR_LEVELS)
                with c_ic:
                    selected_ice = st.selectbox("Đá:", ICE_LEVELS)

                selected_toppings = st.multiselect("Topping:", options=list(TOPPING_OPTIONS.keys()))
            else:
                # Nếu là bánh ngọt thì gán giá trị mặc định (không tính size, đường, đá, topping)
                selected_size = "S (Vừa)"
                selected_sugar = "-"
                selected_ice = "-"
                selected_toppings = []
                st.info("🍰 Bánh ngọt dùng nguyên vị, không cần chọn Size/Đường/Đá.")

        # HIỂN THỊ HÌNH TỰ ĐỘNG THAY ĐỔI KHI BẤM CHỌN MÓN
        with c_preview:
            st.write("**Hình ảnh minh họa:**")
            st.image(item_info["img"], caption=f"{selected_item_name}", use_container_width=True)

        # Tính đơn giá và thành tiền
        if "BÁNH" not in selected_category:
            unit_price = base_price + SIZE_OPTIONS[selected_size] + sum(TOPPING_OPTIONS[t] for t in selected_toppings)
        else:
            unit_price = base_price

        item_total = unit_price * quantity

        st.info(f"💡 Đơn giá: **{unit_price:,} VNĐ** | Thành tiền: **{item_total:,} VNĐ**")

        if st.button("➕ Thêm vào giỏ hàng", type="primary", use_container_width=True):
            topping_str = ", ".join(selected_toppings) if selected_toppings else "Không"
            item_data = {
                "Tên món": selected_item_name,
                "Size": selected_size.split()[0] if "BÁNH" not in selected_category else "-",
                "Đường": selected_sugar.split()[0] if "BÁNH" not in selected_category else "-",
                "Đá": selected_ice.split()[0] if "BÁNH" not in selected_category else "-",
                "Topping": topping_str,
                "Đơn giá": unit_price,
                "Số lượng": quantity,
                "Thành tiền": item_total
            }
            st.session_state.cart.append(item_data)
            st.session_state.invoice_paid = False
            st.toast(f"Đã thêm **{quantity}x {selected_item_name}**!", icon="✅")

    # ==================== CỘT PHẢI: GIỎ HÀNG & THANH TOÁN ====================
    with col_right:
        st.subheader("🛒 Giỏ hàng của bạn")

        if not st.session_state.cart:
            st.warning("Giỏ hàng đang trống. Vui lòng chọn món ở cột bên trái.")
        else:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.dataframe(
                df_cart[["Tên món", "Size", "Topping", "Số lượng", "Đơn giá", "Thành tiền"]],
                use_container_width=True,
                hide_index=True
            )

            if st.button("🗑️ Xóa tất cả món"):
                st.session_state.cart = []
                st.session_state.invoice_paid = False
                st.rerun()

            st.divider()

            # Tự động giảm giá theo hạng thành viên
            auto_discount = 0
            if "VIP" in cust_tier:
                auto_discount = 10
            elif "HSSV" in cust_tier:
                auto_discount = 5

            total_price = df_cart["Thành tiền"].sum()
            
            c_dc, c_py = st.columns(2)
            with c_dc:
                discount = st.number_input("Giảm giá (%):", min_value=0, max_value=100, value=auto_discount, step=5)
            with c_py:
                pay_method = st.selectbox("Hình thức:", ["Tiền mặt 💵", "Chuyển khoản QR 💳", "Ví MoMo 📱"])

            final_price = int(total_price * (1 - discount / 100))

            st.write(f"### Tổng tiền món: **{total_price:,} VNĐ**")
            st.write(f"## TỔNG THANH TOÁN: :red[{final_price:,} VNĐ]")

            if st.button("💳 XÁC NHẬN THANH TOÁN", type="primary", use_container_width=True):
                st.session_state.invoice_paid = True
                st.session_state.order_history.append({
