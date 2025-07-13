import streamlit as st
from PIL import Image
import os
import pandas as pd
from datetime import datetime

# ---- DATA ----
menu = {
    "chả và đồ ăn chế biến sẵn": {
        "Chả Bò": 14,
        "Chả Cá Măng (chiên sẵn)": 12,
        "Chả Huế nhỏ": 2.5,
        "Chả Huế lớn": 12,
        "Giò Sống": 12,
        "Nem Nướng Sống": 20,
        "Chả Mực": 18,
        "Chả Ốc": 2.5,
        "Chả Lụa": 12,
        "Chả Lụa Ớt": 12,
        "Chả Lụa Bì": 12,
        "Chả Chiên": 13,
        "Nem Chua": 9,
        "Cá Lù Đù Phile Muối Sả Ớt": 17,
        "Đùi Sả": 14,
        "Heo Rừng Xào Lăn": 31,
        "Dẻ Ướp Nướng": 31,
        "Bò Lá Lốt (20 cái)": 25,
        "Chạo Tôm Bọc Mía (6 cây)": 23,
        "Hoành Thánh Tôm Thịt (30 cái)": 21,
        "Chả Giò (15 cái)": 20,
        "Bánh Nậm (12 cái)": 16,
        "Bánh Bột Lọc (25 cái)": 23,
        "Bò Kho": 17,
        "Bánh bao mặn (8 cái)": 15,
        "Bánh bao gà nấm (8 cái)": 15,
        "Bánh bao chay (8 cái)": 15,
        "Bánh bao cade (8 cái)": 17,
        "Bánh bao khoai môn (8 cái)": 15
    },
    "rau và trái cây": {
        "Cải xanh": 3,
        "Xà lách": 2.5,
        "Dưa leo": 2,
        "Chuối": 1.5,
        "Cam sành": 2.5
    },
    "thịt và cá": {
        "Thịt ba chỉ": 6,
        "Thịt bò xay": 8,
        "Cánh gà": 7,
        "Cá basa phi lê": 5,
        "Tôm sú": 12
    }
}

# ---- THÀNH PHẦN MÓN ĂN ----
ingredient_info = {
    "Chả Bò": "Thịt bò, tiêu, nước mắm, tỏi, hành",
    "Nem Nướng Sống": "Thịt heo xay, hành tím, nước mắm, tiêu",
    "Chả Mực": "Mực tươi, thì là, tiêu, muối",
    "Chả Giò": "Thịt heo, miến, mộc nhĩ, cà rốt, hành tím",
    "Bánh bao chay (8 cái)": "Bột mì, nấm mèo, miến, cà rốt, đậu hũ"
    # Có thể thêm nhiều món hơn tại đây
}

st.set_page_config(page_title="Menu Mua Hàng - Hai Long", layout="wide")
st.title("🛒 HAI LONG – MENU ĐẶT HÀNG")
st.markdown("Vui lòng chọn các mặt hàng bạn muốn mua từ các tab dưới đây:")

# ---- TABS ----
tabs = st.tabs(["🥢 Chả & Đồ ăn chế biến sẵn", "🥬 Rau & Trái Cây", "🥩 Thịt & Cá", "📋 Bảng thành phần các món ăn"])
selections = []

image_dir = "Image"

def image_filename(item_name):
    clean = item_name.lower()
    for c in ["(", ")", ",", "-", "/"]:
        clean = clean.replace(c, " ")
    clean = clean.replace("đ", "d").replace("ớ", "o").replace("ư", "u").replace("à", "a")
    clean = "_".join(clean.split())
    return os.path.join(image_dir, f"{clean}.jpg")

for idx, category in enumerate(menu.keys()):
    with tabs[idx]:
        st.subheader(category.upper())

        for item, price in menu[category].items():
            col1, col2 = st.columns([1, 2])
            with col1:
                img_path = image_filename(item)
                if os.path.exists(img_path):
                    st.image(img_path, width=100)
                else:
                    st.caption("(Không tìm thấy ảnh)")
            with col2:
                checkbox = st.checkbox(f"{item} (${price}/phần)", key=f"{category}_{item}")
                quantity = st.number_input(
                    f"Số lượng - {item}", min_value=0, max_value=100, step=1, key=f"qty_{category}_{item}"
                )
                if checkbox and quantity > 0:
                    selections.append({"item": item, "price": price, "quantity": quantity})

# ---- THÀNH PHẦN ----
with tabs[3]:
    st.subheader("📋 BẢNG THÀNH PHẦN CÁC MÓN ĂN")
    for item, desc in ingredient_info.items():
        st.markdown(f"**{item}**: {desc}")

# ---- FORM ----
st.markdown("---")
st.subheader("🔒 Thông tin đặt hàng")
with st.form("order_form"):
    customer_name = st.text_input("Họ và tên")
    store_name = st.text_input("Tên tiệm")
    submitted = st.form_submit_button("Gửi đơn hàng")

    if submitted:
        if not customer_name or not store_name:
            st.warning("Vui lòng nhập đầy đủ họ tên và tên tiệm!")
        elif not selections:
            st.warning("Bạn chưa chọn mặt hàng nào!")
        else:
            st.success(f"Cảm ơn {customer_name} từ {store_name}! Đây là đơn hàng của bạn:")

            total = 0
            order_details = []
            for s in selections:
                item_total = s["price"] * s["quantity"]
                total += item_total
                st.write(f"- {s['item']}: {s['quantity']} x ${s['price']} = ${item_total:.2f}")
                order_details.append({
                    "Khách hàng": customer_name,
                    "Tên tiệm": store_name,
                    "Món": s["item"],
                    "Số lượng": s["quantity"],
                    "Đơn giá": s["price"],
                    "Thành tiền": item_total,
                    "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            st.markdown(f"## 🧾 Tổng cộng: **${total:.2f}**")
            st.balloons()

            # Lưu đơn hàng vào file CSV
            df = pd.DataFrame(order_details)
            if not os.path.exists("orders.csv"):
                df.to_csv("orders.csv", index=False)
            else:
                df.to_csv("orders.csv", mode="a", header=False, index=False)

# ---- IMAGE LOCATION INSTRUCTIONS ----
st.sidebar.header("📸 Hướng dẫn thêm hình ảnh")
st.sidebar.markdown("👉 Đặt ảnh trong thư mục `Image/` cùng cấp với file này.")
st.sidebar.markdown("Tên file ảnh cần viết thường, không dấu, nối bằng gạch dưới, ví dụ:")
st.sidebar.code("""
Image/nem_nuong_song.jpg
Image/cha_bo.jpg
Image/banh_bao_chay.jpg
""")
