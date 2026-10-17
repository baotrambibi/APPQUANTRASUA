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
# 4. CHỨC NĂNG 1: ORDER BÁN HÀNG
# ---------------------------------------------------------
if nav_choice == "🛒 Order Bán Hàng":

    st.title("☕ BI COFFEE & TEA 🌿")
    st.caption("Hệ thống tính tiền và gọi món nhanh chóng")
    st.divider()

    col_left, col_right = st.columns([1.2, 0.8])

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

        selected_category = st.radio(
            "Danh mục món:", 
            list(MENU_ITEMS.keys()), 
            horizontal=True
        )

        category_dict = MENU_ITEMS[selected_category]

        # Chia 2 cột: Cột trái chọn thông tin, Cột phải hiện hình ảnh minh họa thay đổi theo món
        c_select, c_preview = st.columns([1.2, 1])

        with c_select:
            selected_item_name = st.selectbox("Tên món:", list(category_dict.keys()))
            item_info = category_dict[selected_item_name]
            base_price = item_info["price"]

            quantity = st.number_input("Số lượng:", min_value=1, value=1, step=1)

            c_sz, c_sg, c_ic = st.columns(3)
            with c_sz:
                selected_size = st.selectbox("Size:", list(SIZE_OPTIONS.keys()))
            with c_sg:
                selected_sugar = st.selectbox("Đường:", SUGAR_LEVELS)
            with c_ic:
                selected_ice = st.selectbox("Đá:", ICE_LEVELS)

            selected_toppings = st.multiselect("Topping:", options=list(TOPPING_OPTIONS.keys()))

        # HIỂN THỊ HÌNH ẢNH THAY ĐỔI DỰA TRÊN MÓN ĐƯỢC CHỌN
        with c_preview:
            st.write("**Hình ảnh minh họa:**")
            st.image(item_info["img"], caption=f"{selected_item_name}", use_container_width=True)

        # Tính tiền
        unit_price = base_price + SIZE_OPTIONS[selected_size] + sum(TOPPING_OPTIONS[t] for t in selected_toppings)
        item_total = unit_price * quantity

        st.info(f"💡 Đơn giá 1 ly: **{unit_price:,} VNĐ** | Thành tiền: **{item_total:,} VNĐ**")

        if st.button("➕ Thêm vào giỏ hàng", type="primary", use_container_width=True):
            topping_str = ", ".join(selected_toppings) if selected_toppings else "Không"
            item_data = {
                "Tên món": selected_item_name,
                "Size": selected_size.split()[0],
                "Đường": selected_sugar.split()[0],
                "Đá": selected_ice.split()[0],
                "Topping": topping_str,
                "Đơn giá": unit_price,
                "Số lượng": quantity,
                "Thành tiền": item_total
            }
            st.session_state.cart.append(item_data)
            st.session_state.invoice_paid = False
            st.toast(f"Đã thêm **{quantity}x {selected_item_name}**!", icon="✅")

    with col_right:
        st.subheader("🛒 Giỏ hàng của bạn")

        if not st.session_state.cart:
            st.warning("Giỏ hàng đang trống.")
        else:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.dataframe(
                df_cart[["Tên món", "Size", "Topping", "Số lượng", "Thành tiền"]],
                use_container_width=True,
                hide_index=True
            )

            if st.button("🗑️ Xóa tất cả món"):
                st.session_state.cart = []
                st.session_state.invoice_paid = False
                st.rerun()

            st.divider()

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
                pay_method = st.selectbox("Thanh toán:", ["Tiền mặt 💵", "Chuyển khoản QR 💳", "Ví MoMo 📱"])

            final_price = int(total_price * (1 - discount / 100))

            st.write(f"### Tổng tiền món: **{total_price:,} VNĐ**")
            st.write(f"## TỔNG THANH TOÁN: :red[{final_price:,} VNĐ]")

            if st.button("💳 XÁC NHẬN THANH TOÁN", type="primary", use_container_width=True):
                st.session_state.invoice_paid = True
                st.session_state.order_history.append({
                    "time": datetime.now().strftime("%H:%M:%S - %d/%m/%Y"),
                    "customer": customer_name if customer_name else "Khách vãng lai",
                    "type": service_type,
                    "items_count": len(st.session_state.cart),
                    "total": final_price,
                    "details": st.session_state.cart
                })
                st.balloons()

    if st.session_state.get("invoice_paid") and st.session_state.cart:
        st.divider()
        st.success("🎉 Thanh toán thành công! Chi tiết hóa đơn:")

        c_inv, c_qr = st.columns([1.2, 0.8])
        
        with c_inv:
            st.markdown("### ☕ BI COFFEE & TEA")
            st.write(f"**Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            st.write(f"**Khách hàng:** {customer_name if customer_name else 'Khách vãng lai'} ({service_type})")
            st.table(pd.DataFrame(st.session_state.cart)[["Tên món", "Size", "Đường", "Đá", "Topping", "Số lượng", "Thành tiền"]])
            st.write(f"### **TỔNG THANH TOÁN: {final_price:,} VNĐ**")

        with c_qr:
            if "Chuyển khoản" in pay_method or "MoMo" in pay_method:
                st.markdown("#### 📱 Mã QR Thanh Toán")
                qr_url = f"https://img.vietqr.io/image/MB-0123456789-compact2.png?amount={final_price}&addInfo=BiCoffee"
                st.image(qr_url, caption="Mở App Ngân hàng quét mã", use_container_width=True)

        if st.button("🔄 Tạo đơn mới", use_container_width=True):
            st.session_state.cart = []
            st.session_state.invoice_paid = False
            st.rerun()

# ---------------------------------------------------------
# 5. CHỨC NĂNG 2: MÀN HÌNH PHA CHẾ
# ---------------------------------------------------------
elif nav_choice == "👨‍🍳 Màn Hình Pha Chế":
    st.title("👨‍🍳 Màn Hình Pha Chế (Barista)")
    st.divider()

    if not st.session_state.order_history:
        st.info("Chưa có đơn hàng nào.")
    else:
        for idx, order in enumerate(reversed(st.session_state.order_history), 1):
            with st.expander(f"📦 Đơn #{len(st.session_state.order_history)-idx+1} - {order['customer']} ({order['type']}) - {order['time']}", expanded=True):
                for item in order["details"]:
                    st.write(f"- **{item['Số lượng']}x {item['Tên món']}** (Size: {item['Size']} | Đường: {item['Đường']} | Đá: {item['Đá']} | Topping: {item['Topping']})")
                if st.button(f"✅ Đã xong đơn #{len(st.session_state.order_history)-idx+1}", key=f"kds_{idx}"):
                    st.toast("Đã chuyển đơn!", icon="☕")

# ---------------------------------------------------------
# 6. CHỨC NĂNG 3: BÁO CÁO DOANH THU
# ---------------------------------------------------------
elif nav_choice == "📊 Doanh Thu & Lịch Sử":
    st.title("📊 Doanh Thu & Lịch Sử Đơn Hàng")
    st.divider()

    if not st.session_state.order_history:
        st.warning("Chưa có lịch sử bán hàng.")
    else:
        total_rev = sum(o["total"] for o in st.session_state.order_history)
        total_orders = len(st.session_state.order_history)

        m1, m2 = st.columns(2)
        m1.metric("Tổng Doanh Thu", f"{total_rev:,} VNĐ")
        m2.metric("Tổng Số Đơn Hàng", f"{total_orders} Đơn")

        st.divider()
        df_history = pd.DataFrame(st.session_state.order_history)
        st.dataframe(df_history[["time", "customer", "type", "items_count", "total"]], use_container_width=True)
