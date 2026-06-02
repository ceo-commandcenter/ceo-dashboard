import streamlit as st
import requests
import google.generativeai as genai

# --- KEYS SETUP (WITH JOINED TOKEN) ---
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
GREEN_API_INSTANCE = st.secrets.get("GREEN_API_INSTANCE", "")

# Token ke dono parts ko jod kar poora token banana
PART1 = st.secrets.get("PART1", "")
PART2 = st.secrets.get("PART2", "")
GREEN_API_TOKEN = PART1 + PART2

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="CEO Command Center", layout="wide")
st.title("💼 CEO Command Center: AI Empire")
st.write("🚀 Team Status: Active and Monitoring...")

# --- DATA STORAGE ---
if "orders" not in st.session_state: st.session_state.orders = {}
if "leads" not in st.session_state: st.session_state.leads = []

# --- ROHAN (SIDEBAR) ---
with st.sidebar:
    st.header("📢 Rohan (Marketing Manager)")
    if st.button("🔍 Rohan: Find Handicraft Buyers"):
        try:
            model = genai.GenerativeModel('gemini-pro')
            res = model.generate_content("Generate a list of 3 potential Indian handicraft buyers and store names.")
            st.session_state.leads.append(res.text)
            st.success("Leads generated!")
        except Exception as e: st.error(f"Error: {e}")
            
    if st.session_state.leads:
        for idx, lead in enumerate(st.session_state.leads):
            st.info(f"Lead Set #{idx+1}\n{lead}")

# --- 📲 WHATSAPP ENGINE ---
if GREEN_API_INSTANCE and GREEN_API_TOKEN:
    try:
        receive_url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/receiveNotification/{GREEN_API_TOKEN}"
        res = requests.get(receive_url, timeout=4).json()
        
        if res and "receiptId" in res:
            receipt_id = res["receiptId"]
            body = res.get("body", {})
            
            if body.get("typeWebhook") == "incomingMessageReceived":
                user_msg = body.get("messageData", {}).get("textMessageData", {}).get("textMessage", "")
                sender_id = body.get("senderData", {}).get("chatId", "")
                
                if user_msg and sender_id:
                    amit_persona = (
                        "Aapka naam Amit hai aur aap Sales Manager hain. Tameez se 'Sir/Ma'am' kehkar baat karein. "
                        "Client ko kahein: 'Maine details CEO Sir ke dashboard par bhej di hain, jaise hi sir final price batayenge main aapko confirm karta hoon. Tab tak aap advance payment ready rakhein.' "
                        "Aapko khud se koi price nahi batana hai."
                    )
                    
                    if any(k in user_msg.lower() for k in ["order", "product", "deal", "buy", "price", "kharidna", "rate", "bhaav"]):
                        st.session_state.orders[sender_id] = {"client": sender_id, "msg": user_msg, "status": "pending_price", "price": None}
                    
                    model = genai.GenerativeModel('gemini-pro')
                    ai_res = model.generate_content(f"{amit_persona}\n\nClient: {user_msg}\nAmit:")
                    
                    send_url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
                    requests.post(send_url, json={"chatId": sender_id, "message": ai_res.text})
            
            requests.delete(f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/deleteNotification/{GREEN_API_TOKEN}/{receipt_id}")
            st.rerun()
    except:
        pass

# --- MAIN DASHBOARD LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    st.header("🤝 Amit (Sales Manager)")
    if not st.session_state.orders:
        st.info("Abhi tak koi pending product query nahi aayi hai.")
    else:
        for client_id, order_data in list(st.session_state.orders.items()):
            if order_data['status'] == 'pending_price':
                st.warning(f"📦 **Naya Product Mila** from `{client_id}`")
                st.write(f"**Details:** {order_data['msg']}")
                
                ceo_price = st.text_input(f"Iska price set karein (₹):", key=f"p_{client_id}")
                if st.button(f"Confirm Price & Send", key=f"btn_{client_id}"):
                    if ceo_price:
                        st.session_state.orders[client_id]['price'] = ceo_price
                        st.session_state.orders[client_id]['status'] = 'price_sent'
                        
                        url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
                        reply = f"Amit here! CEO Sir ne is product ka price ₹{ceo_price} confirm kar diya hai. Kripya advance payment process kijiye."
                        requests.post(url, json={"chatId": client_id, "message": reply})
                        st.success("Price bhej diya gaya!")
                        st.rerun()

with col2:
    st.header("🧮 C.A. Sharma Ji")
    completed_orders = [o for o in st.session_state.orders.values() if o['status'] == 'price_sent']
    if completed_orders:
        if st.button("📊 Sharma Ji: Calculate Profit & Bill"):
            try:
                model = genai.GenerativeModel('gemini-pro')
                sharma_prompt = f"Aap C.A. Sharma Ji hain. In orders ka 30% profit nikaliye aur Indian invoice format banaiye: {str(completed_orders)}"
                res = model.generate_content(sharma_prompt)
                st.code(res.text, language="text")
            except Exception as e: st.error(f"Error: {e}")
    else:
        st.info("Deals poori hone par Sharma Ji yahan bill banayenge.")

if st.button("🔄 Check New WhatsApp Messages manually"):
    st.rerun()
