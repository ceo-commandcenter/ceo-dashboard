import streamlit as st
import requests
import google.generativeai as genai

# --- KEYS SETUP ---
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
GREEN_API_INSTANCE = st.secrets.get("GREEN_API_INSTANCE", "")
GREEN_API_TOKEN = st.secrets.get("GREEN_API_TOKEN", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="CEO Command Center", layout="wide")
st.title("💼 CEO Command Center: AI Empire")
st.write("🚀 Aapki company ke teeno AI Agents sahi jagah par set hain aur active hain!")

# --- DATA STORAGE (SESSION STATE) ---
if "orders" not in st.session_state:
    st.session_state.orders = {}
if "leads" not in st.session_state:
    st.session_state.leads = []

# --- SIDEBAR: ROHAN (MARKETING MANAGER) ---
with st.sidebar:
    st.header("📢 Rohan (Marketing Manager)")
    st.write("Rohan ka kaam hai naye Indian Handicraft buyers ko dhoondhna aur leads Amit ko dena.")
    
    if st.button("🔍 Rohan: Find Handicraft Buyers"):
        try:
            model = genai.GenerativeModel('gemini-pro')
            res = model.generate_content("Generate a crisp, bulleted list of 3 potential Indian handicraft buyers, their store/company names, and location for our sales manager Amit.")
            st.session_state.leads.append(res.text)
            st.success("Rohan ne naye buyers dhoondh liye hain!")
        except Exception as e:
            st.error(f"Error: {e}")
            
    if st.session_state.leads:
        st.subheader("📋 Amit ke liye New Leads:")
        for idx, lead in enumerate(st.session_state.leads):
            st.info(f"Lead Set #{idx+1}\n{lead}")

# --- MAIN SCREEN: AMIT & SHARMA JI ---
col1, col2 = st.columns(2)

# 1. AMIT (SALES MANAGER)
with col1:
    st.header("🤝 Amit (Sales Manager)")
    st.write("Amit WhatsApp par client se deal kar raha hai. Jab koi naya product ya order aayega, toh woh aapse price poochega:")
    
    if not st.session_state.orders:
        st.info("Abhi tak WhatsApp par koi naya product request nahi aaya hai.")
    else:
        for client_id, order_data in list(st.session_state.orders.items()):
            if order_data['status'] == 'pending_price':
                st.warning(f"📦 **Naya Product Mila** from Client: `{client_id}`")
                st.write(f"**Client ka message:** {order_data['msg']}")
                
                # CEO inputs price here
                ceo_price = st.text_input(f"Is product ka kya price rakhna hai? (₹):", key=f"p_{client_id}")
                if st.button(f"Confirm Price & Send to Client", key=f"btn_{client_id}"):
                    if ceo_price:
                        # Update status
                        st.session_state.orders[client_id]['price'] = ceo_price
                        st.session_state.orders[client_id]['status'] = 'price_sent'
                        
                        # Send price to WhatsApp via Green API
                        url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
                        reply_text = f"Amit here! Maine CEO Sir se baat kar li hai. Unhone is product ka price ₹{ceo_price} set kiya hai. Kripya deal confirm karne ke liye advance payment process kijiye."
                        requests.post(url, json={"chatId": client_id, "message": reply_text})
                        st.success(f"Price ₹{ceo_price} Amit ne client ko WhatsApp par bhej diya!")
                        st.rerun()

# 2. C.A. SHARMA JI (FINANCE & BILLING)
with col2:
    st.header("🧮 C.A. Sharma Ji")
    st.write("Sharma Ji yahan aapke saare munafe (profit) ka hisab aur billing dekhte hain.")
    
    # Active/Completed orders list for Sharma Ji
    completed_orders = [o for o in st.session_state.orders.values() if o['status'] == 'price_sent']
    if completed_orders:
        if st.button("📊 Sharma Ji: Hisab Lagao aur Bill Banao"):
            try:
                model = genai.GenerativeModel('gemini-pro')
                order_summary = str(completed_orders)
                sharma_prompt = (
                    f"Aap C.A. Sharma Ji hain, ek anubhavi Indian accountant. Niche diye gaye orders ka profit margin (30% ke hisab se) "
                    f"calculate kijiye aur ek badhiya Indian business format (Invoice) mein bill draft kijiye. Beech mein thodi apni "
                    f"shant 'Sharma Ji' wali bhasha (beta, bhai sahab, munafa) ka use kijiye:\n{order_summary}"
                )
                res = model.generate_content(sharma_prompt)
                st.code(res.text, language="text")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("Jaise hi Amit koi deal ka price bhejega, Sharma Ji uska bill aur profit yahan nikal denge.")

# --- 📲 WHATSAPP HANDLER ---
if GREEN_API_INSTANCE and GREEN_API_TOKEN:
    try:
        receive_url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/receiveNotification/{GREEN_API_TOKEN}"
        response = requests.get(receive_url, timeout=2).json()
        
        if response and "receiptId" in response:
            receipt_id = response["receiptId"]
            body = response.get("body", {})
            
            if body.get("typeWebhook") == "incomingMessageReceived":
                message_data = body.get("messageData", {})
                text_message_data = message_data.get("textMessageData", {})
                user_msg = text_message_data.get("textMessage", "")
                sender_id = body.get("senderData", {}).get("chatId", "")
                
                if user_msg and sender_id:
                    # Persona for Amit
                    amit_persona = (
                        "Aapka naam Amit hai aur aap Sales Manager hain. Aap WhatsApp par client se bohot tameez aur izzat se baat karte hain (Sir/Ma'am use karein). "
                        "Agar client kisi naye product, order ya rate ke baare mein poochta hai, toh aapko bolna hai: "
                        "'Main yeh details abhi apne CEO sir ke dashboard par bhej raha hoon. Jaise hi sir mujhe iska final price batayenge, main aapko turant confirm karunga. Tab tak aap advance payment ready rakhiye.' "
                        "Aapko khud se koi price nahi batana hai."
                    )
                    
                    is_product_query = any(k in user_msg.lower() for k in ["order", "product", "deal", "buy", "price", "kharidna", "bhaav", "rate", "kitne ka"])
                    
                    if is_product_query and sender_id not in st.session_state.orders:
                        st.session_state.orders[sender_id] = {"client": sender_id, "msg": user_msg, "status": "pending_price", "price": None}
                    
                    # Generate reply via Gemini
                    model = genai.GenerativeModel('gemini-pro')
                    full_prompt = f"{amit_persona}\n\nClient ne kaha: '{user_msg}'\nAmit ka jawab:"
                    ai_response = model.generate_content(full_prompt)
                    ai_reply = ai_response.text
                    
                    # Send response back to WhatsApp
                    send_url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
                    requests.post(send_url, json={"chatId": sender_id, "message": ai_reply})
            
            # Delete notification
            delete_url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/deleteNotification/{GREEN_API_TOKEN}/{receipt_id}"
            requests.delete(delete_url)
            st.rerun()
            
    except Exception as e:
        pass
