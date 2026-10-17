import streamlit as st
import pandas as pd
from datetime import datetime
import random
import streamlit.components.v1 as components

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Bi Coffee & Tea - Smart POS System",
    page_icon="☕",
    layout="wide"
)

# ---------------------------------------------------------
# 2. MENU SẢN PHẨM & DỮ LIỆU
# ---------------------------------------------------------
MENU_ITEMS = {
    "☕ CÀ PHÊ": {
        "Cà Phê Đen Đá": {
            "price": 25000,
            "img": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500",
            "tags": ["mệt mỏi", "đậm vị", "tỉnh táo"]
        },
        "Cà Phê Sữa Đá": {
            "price": 28000,
            "img": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500",
            "tags": ["ngọt ngào", "tỉnh táo"]
        },
        "Bạc Xỉu": {
            "price": 32000,
            "img": "https://images.unsplash.com/photo-1541167760496-1628856ab772?w=500",
            "tags": ["béo béo", "nhẹ nhàng"]
        },
        "Matcha Espresso Latte": {
            "price": 42000,
            "img": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=500",
            "tags": ["độc lạ", "đậm vị"]
        }
    },
    "🧋 TRÀ & TRÀ SỮA": {
        "Matcha Latte": {
            "price": 40000,
            "img": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=500",
            "tags": ["béo béo", "thư giãn"]
        },
        "Trà Sữa Trân Châu Đường Đen": {
            "price": 35000,
            "img": "https://images.unsplash.com/photo-1558857563-b371033873b8?w=500",
            "tags": ["ngọt ngào", "vui vẻ"]
        },
        "Trà Sữa Thái Xanh": {
            "price": 32000,
            "img": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=500",
            "tags": ["sảng khoái", "thanh mát"]
        },
        "Trà Đào Cam Sả": {
            "price": 35000,
            "img": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=500",
            "tags": ["nắng nóng", "thanh mát", "sảng khoái"]
        },
        "Trà Dâu Tằm": {
            "price": 32000,
            "img": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500",
            "tags": ["thanh mát", "chua ngọt"]
        }
    },
    "🍰 BÁNH & NGỌT": {
        "Bánh Croissant Bơ Tỏi": {
            "price": 29000,
            "img": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=500",
            "tags": ["ăn nhẹ", "thơm bơ"]
        },
        "Bánh Tiramisu": {
            "price": 35000,
            "img": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=500",
            "tags": ["ngọt ngào", "mềm mịn"]
        }
    }
}

SIZE_OPTIONS = {"S (Vừa)": 0, "M (Lớn)": 5000, "L (Đặc biệt)": 10000}
TOPPING_OPTIONS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000
}
SUGAR_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0% (Không đường)"]
ICE_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0% (Không đá)"]

# Khởi tạo Session State
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "order_history" not in st.session_state:
    st.session_state.order_history = []
if "lucky_discount" not in st.session_state:
    st.session_state.lucky_discount = 0
if "spin_reward_text" not in st.session_state:
    st.session_state.spin_reward_text = ""

# ---------------------------------------------------------
# HÀM XUẤT HÓA ĐƠN DẠNG TEXT (.TXT)
# ---------------------------------------------------------
def create_txt_invoice(customer_name, service_type, cart, total_amount, discount, final_amount):
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
        content += "\n"
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
    st.caption("Smart POS System v2.0")
    st.divider()

    nav_choice = st.radio(
        "Chức năng:",
        [
            "🛒 Order Bán Hàng",
            "🤖 AI Gợi Ý Món Nước",
            "👨‍🍳 Màn Hình Pha Chế",
            "📊 Doanh Thu & Lịch Sử"
        ]
    )

# ---------------------------------------------------------
# 4. CHỨC NĂNG 1: ORDER BÁN HÀNG & POS
# ---------------------------------------------------------
if nav_choice == "🛒 Order Bán Hàng":

    header_html = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,600&family=Montserrat:wght@400;500&display=swap');
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <div style="
        background: linear-gradient(135deg, #2B1810 0%, #3D2317 50%, #1F110B 100%);
        padding: 28px 30px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.25);
        margin-bottom: 25px;
        border: 1px solid #795548;
    ">
        <h1 style="
            font-family: 'Playfair Display', 'Georgia', serif;
            font-size: 2.6rem;
            font-weight: 700;
            letter-spacing: 2px;
            margin: 0 0 8px 0;
            line-height: 1.2;
            color: #FFB300;
        ">
            <i class="fa-solid fa-mug-hot" style="
                margin-right: 12px;
                background: linear-gradient(45deg, #FFE082, #FFB300);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            "></i>
            <span style="
                background: linear-gradient(45deg, #FFE082, #FFB300, #FFF8E1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
            ">BI COFFEE & TEA</span>
            <i class="fa-solid fa-leaf" style="
                margin-left: 12px;
                font-size: 2rem;
                color: #81C784;
            "></i>
        </h1>
        <p style="
            font-family: 'Montserrat', 'Arial', sans-serif;
            color: #E0C0A8;
            font-size: 1.1rem;
            margin: 0;
            font-style: italic;
            font-weight: 500;
            letter-spacing: 1px;
        ">"Thưởng thức từng ngụm say mê • Gói trọn vị yêu thương"</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

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
        c_select, c_preview = st.columns([1.2, 1])

        with c_select:
            selected_item_name = st.selectbox("Tên món:", list(category_dict.keys()))
            item_info = category_dict[selected_item_name]
            base_price = item_info["price"]

            quantity = st.number_input("Số lượng:", min_value=1, value=1, step=1)

            # Khởi tạo mặc định cho tất cả trường hợp
            selected_size = "S (Vừa)"
            selected_sugar = "-"
            selected_ice = "-"
            selected_toppings = []

            # Nếu là món nước thì hiển thị tùy chọn
            if "BÁNH" not in selected_category:
                c_sz, c_sg, c_ic = st.columns(3)
                with c_sz:
                    selected_size = st.selectbox("Size:", list(SIZE_OPTIONS.keys()))
                with c_sg:
                    selected_sugar = st.selectbox("Đường:", SUGAR_LEVELS)
                with c_ic:
                    selected_ice = st.selectbox("Đá:", ICE_LEVELS)

                selected_toppings = st.multiselect("Topping:", options=list(TOPPING_OPTIONS.keys()))

        with c_preview:
            st.write("**Hình ảnh minh họa:**")
            st.image(item_info["img"], caption=f"{selected_item_name}", use_container_width=True)

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
                st.session_state.lucky_discount = 0
                st.session_state.spin_reward_text = ""
                st.rerun()

            st.divider()

            base_discount = 10 if "VIP" in cust_tier else (5 if "HSSV" in cust_tier else 0)
            
            discount = st.number_input(
                "Giảm giá tổng (%):", 
                min_value=0, 
                max_value=100, 
                value=base_discount + st.session_state.lucky_discount, 
                step=5
            )

            # VÒNG QUAY MAY MẮN TRỰC QUAN HẤP DẪN
            with st.expander("🎡 VÒNG QUAY MAY MẮN (Bấm để thử vận may!)", expanded=False):
                if st.button("💥 QUAY NGAY KHUYẾN MÃI", type="primary", use_container_width=True):
                    rewards = [5, 10, 15, 20]
                    won_discount = random.choice(rewards)
                    st.session_state.lucky_discount = won_discount
                    st.session_state.spin_reward_text = f"🎉 Chúc mừng! Bạn trúng voucher giảm **{won_discount}%**!"
                    st.rerun()

                # Giao diện đồ họa vòng quay
                wheel_html = """
                <div style="text-align: center; margin-top: 10px;">
                    <div style="
                        display: inline-block;
                        width: 140px; height: 140px;
                        border-radius: 50%;
                        border: 6px solid #FFB300;
                        background: conic-gradient(#FF6F00 0deg 90deg, #FFA000 90deg 180deg, #FFC107 180deg 270deg, #FFD54F 270deg 360deg);
                        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                        position: relative;
                        animation: spin 3s ease-out;
                    ">
                        <div style="
                            position: absolute; top: 50%; left: 50%;
                            transform: translate(-50%, -50%);
                            width: 35px; height: 35px;
                            background: white; border-radius: 50%;
                            box-shadow: 0 0 5px rgba(0,0,0,0.5);
                            font-weight: bold; line-height: 35px; color: #333;
                        ">🎁</div>
                    </div>
                </div>
                """
                st.markdown(wheel_html, unsafe_allow_html=True)

            if st.session_state.spin_reward_text:
                st.success(st.session_state.spin_reward_text)

            total_price = df_cart["Thành tiền"].sum()
            pay_method = st.selectbox("Hình thức:", ["Tiền mặt 💵", "Chuyển khoản QR 💳", "Ví MoMo 📱"])
            final_price = int(total_price * (1 - discount / 100))

            st.write(f"### Tổng tiền món: **{total_price:,} VNĐ**")
            st.write(f"## TỔNG THANH TOÁN: :red[{final_price:,} VNĐ]")

            if st.button("💳 XÁC NHẬN THANH TOÁN", type="primary", use_container_width=True):
                st.session_state.invoice_paid = True
                order_info = {
                    "time": datetime.now().strftime("%H:%M:%S - %d/%m/%Y"),
                    "customer": customer_name if customer_name else "Khách vãng lai",
                    "type": service_type,
                    "items_count": len(st.session_state.cart),
                    "total": final_price,
                    "details": st.session_state.cart
                }
                st.session_state.order_history.append(order_info)
                st.balloons()

    # ==================== HÓA ĐƠN & TEM DÁN LY NƯỚC (STICKER) ====================
    if st.session_state.get("invoice_paid") and st.session_state.cart:
        st.divider()
        st.success("🎉 Thanh toán thành công! Dưới đây là chi tiết hóa đơn & mẫu tem dán:")

        c_inv, c_sticker = st.columns([1.2, 0.8])
        
        with c_inv:
            invoice_box = st.container(border=True)
            with invoice_box:
                st.markdown("<h2 style='text-align: center; color: #4A2E19;'>☕ HÓA ĐƠN BÁN HÀNG - BI COFFEE & TEA</h2>", unsafe_allow_html=True)
                st.write(f"**Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                st.write(f"**Khách hàng:** {customer_name if customer_name else 'Khách vãng lai'} ({service_type})")
                
                st.table(pd.DataFrame(st.session_state.cart)[["Tên món", "Size", "Đường", "Đá", "Topping", "Số lượng", "Thành tiền"]])
                
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Tổng tiền món:** {total_price:,} VNĐ")
                    st.write(f"**Giảm giá:** {discount}%")
                with c2:
                    st.markdown(f"### TỔNG CỦA BẠN: <span style='color:red'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)

            if "Chuyển khoản" in pay_method or "MoMo" in pay_method:
                st.markdown("#### 📱 Mã QR Thanh Toán")
                qr_url = f"https://img.vietqr.io/image/MB-0123456789-compact2.png?amount={final_price}&addInfo=BiCoffee%20Thanh%20Toan"
                st.image(qr_url, caption="Mở App Ngân hàng / MoMo để quét", use_container_width=True)

        with c_sticker:
            st.markdown("#### 🏷️ Mẫu Tem Dán Ly Nước (Print Sticker Label)")
            for idx, item in enumerate(st.session_state.cart, 1):
                st.markdown(f"""
                <div style="
                    border: 2px dashed #3E2723;
                    padding: 12px 15px;
                    border-radius: 10px;
                    background-color: #FFFDE7;
                    color: #212121;
                    font-family: 'Courier New', Courier, monospace;
                    margin-bottom: 10px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                ">
                    <div style="text-align: center; font-weight: bold; font-size: 1.1rem; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-bottom: 6px;">
                        [ BI COFFEE & TEA ]
                    </div>
                    <b>Món #{idx}:</b> {item['Tên món']} ({item['Size']})<br/>
                    <b>Tùy chọn:</b> {item['Đường']} đường | {item['Đá']} đá<br/>
                    <b>Topping:</b> {item['Topping']}<br/>
                    <b>Khách:</b> {customer_name if customer_name else 'Khách vãng lai'} ({service_type})<br/>
                    <div style="text-align: right; font-size: 0.8rem; color: #666; margin-top: 4px;">
                        {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        txt_data = create_txt_invoice(customer_name, service_type, st.session_state.cart, total_price, discount, final_price)
        
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                label="📥 Tải hóa đơn (.TXT)",
                data=txt_data,
                file_name=f"HoaDon_BiCoffee_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary"
            )
        with col_dl2:
            if st.button("🔄 Tạo đơn hàng mới", use_container_width=True):
                st.session_state.cart = []
                st.session_state.invoice_paid = False
                st.session_state.lucky_discount = 0
                st.session_state.spin_reward_text = ""
                st.rerun()

# ---------------------------------------------------------
# 5. CHỨC NĂNG 2: AI GỢI Ý MÓN NƯỚC
# ---------------------------------------------------------
elif nav_choice == "🤖 AI Gợi Ý Món Nước":
    st.title("🤖 AI Sommelier - Tư Vấn Món Nước Thông Minh")
    st.caption("Khám phá đồ uống phù hợp nhất dựa trên tâm trạng & thời tiết của bạn!")
    st.divider()

    c_mood, c_weather = st.columns(2)
    with c_mood:
        mood = st.selectbox("Hôm nay tâm trạng bạn thế nào?", ["Tươi vui 🥳", "Mệt mỏi 😴", "Cần tập trung 🧠", "Thèm ngọt 🍫"])
    with c_weather:
        weather = st.selectbox("Thời tiết bên ngoài ra sao?", ["Nắng nóng ☀️", "Trời mưa 🌧️", "Mát mẻ 🍃"])

    if st.button("✨ AI Đề Xuất Đồ Uống", type="primary"):
        st.markdown("---")
        st.subheader("💡 Đồ uống AI khuyên dùng riêng cho bạn:")
        
        suggested = []
        for cat, items in MENU_ITEMS.items():
            for name, info in items.items():
                suggested.append((name, info))

        sample_items = random.sample(suggested, min(2, len(suggested)))
        cols = st.columns(len(sample_items))
        for idx, (name, info) in enumerate(sample_items):
            with cols[idx]:
                st.image(info["img"], use_container_width=True)
                st.markdown(f"### {name}")
                st.write(f"**Giá:** {info['price']:,} VNĐ")
                st.caption(f"Lý do: Rất thích hợp với trạng thái '{mood}' & không khí '{weather}'.")

# ---------------------------------------------------------
# 6. CHỨC NĂNG 3: MÀN HÌNH PHA CHẾ BARISTA
# ---------------------------------------------------------
elif nav_choice == "👨‍🍳 Màn Hình Pha Chế":
    st.title("👨‍🍳 Màn Hình Pha Chế (Barista KDS)")
    st.divider()

    if not st.session_state.order_history:
        st.info("Chưa có đơn hàng nào cần làm.")
    else:
        for idx, order in enumerate(reversed(st.session_state.order_history), 1):
            with st.expander(f"📦 Đơn #{len(st.session_state.order_history)-idx+1} - {order['customer']} ({order['type']}) - Lúc {order['time']}", expanded=True):
                for item in order["details"]:
                    st.write(f"- **{item['Số lượng']}x {item['Tên món']}** (Size: {item['Size']} | Đường: {item['Đường']} | Đá: {item['Đá']} | Topping: {item['Topping']})")
                if st.button(f"✅ Hoàn thành đơn #{len(st.session_state.order_history)-idx+1}", key=f"kds_{idx}"):
                    st.toast("Đã hoàn thành đơn!", icon="☕")

# ---------------------------------------------------------
# 7. CHỨC NĂNG 4: BÁO CÁO DOANH THU
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
