import streamlit as st
import requests

# --- KEYS SETUP ---
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
GREEN_API_INSTANCE = st.secrets.get("GREEN_API_INSTANCE", "")
GREEN_API_TOKEN = st.secrets.get("GREEN_API_TOKEN", "")

st.set_page_config(page_title="CEO Command Center", layout="wide")
st.title("💼 CEO Command Center: AI Empire")
st.write("🚀 Team Status: Active and Monitoring...")

# --- DATA STORAGE ---
if "orders" not in st.session_state: st.session_state.orders = {}
if "leads" not in st.session_state: st.session_state.leads = []

# --- 🧠 DIRECT GEMINI API CALL FUNCTION (NO LIBRARY NEEDED) ---
def call_gemini(prompt_text):
    if not GEMINI_API_KEY:
        return "Error: Gemini API Key missing in Secrets!"
    # Direct HTTP Request to Google API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        res_json = response.json()
        return res_json['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Google Server Error: {e}"

# --- 📢 ROHAN (MARKETING MANAGER) ---
with st.sidebar:
    st.header("📢 Rohan (Marketing Manager)")
    if st.button("🔍 Rohan: Find Handicraft Buyers"):
        try:
            with st.spinner("Rohan buyers dhoond raha hai..."):
                report = call_gemini("Generate a list of 3 potential Indian handicraft buyers and store names with locations.")
                st.session_state.leads.append(report)
                st.success("Leads generated!")
        except Exception as e: 
            st.error(f"Rohan Error: {e}")
            
    if st.session_state.leads:
        for idx, lead in enumerate(st.session_state.leads):
            st.info(f"Lead Set #{idx+1}\n{lead}")

# --- 📲 WHATSAPP ENGINE ---
if GREEN_API_INSTANCE and GREEN_API_TOKEN:
    try:
        receive_url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/receiveNotification/{GREEN_API_TOKEN}"
        response = requests.get(receive_url, timeout=3)
        
        if response.status_code == 200 and response.text.strip():
            res = response.json()
            if res and "receiptId" in res:
                receipt_id = res["receiptId"]
                body = res.get("body", {})
                
                if body.get("typeWebhook") == "incomingMessageReceived":
                    user_msg = body.get("messageData", {}).get("textMessageData", {}).get("textMessage", "")
                    sender_id = body.get("senderData", {}).get("chatId", "")
                    
                    if user_msg and sender_id:
                        if any(k in user_msg.lower() for k in ["order", "product", "deal", "buy", "price", "kharidna", "rate", "hello", "hi"]):
                            st.session_state.orders[sender_id] = {"client": sender_id, "msg": user_msg, "status": "pending_price"}
                            
                            amit_persona = "Aapka naam Amit hai, Sales Manager. Client ko bohot polite bhasha mein kahein ki unka message CEO sir ke dashboard par chala gaya hai, jaise hi sir price batayenge hum aapko confirm karenge."
                            ai_reply = call_gemini(f"{amit_persona}\n\nClient: {user_msg}\nAmit:")
                            
                            send_url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
                            requests.post(send_url, json={"chatId": sender_id, "message": ai_reply})
                
                requests.delete(f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/deleteNotification/{GREEN_API_TOKEN}/{receipt_id}")
                st.rerun()
    except Exception:
        pass

# --- MAIN DASHBOARD LAYOUT (AMIT & SHARMA JI) ---
col1, col2 = st.columns(2)

with col1:
    st.header("🤝 Amit (Sales Manager)")
    
    if st.button("🧪 Simulated Test: Generate Dummy Order"):
        dummy_id = "919999999999@c.us"
        st.session_state.orders[dummy_id] = {"client": dummy_id, "msg": "Mujhe 50 items ka price janna hai, urgently batayein.", "status": "pending_price"}
        st.rerun()

    if not st.session_state.orders:
        st.info("Koi pending product request nahi hai abhi.")
    else:
        for client_id, order_data in list(st.session_state.orders.items()):
            st.warning(f"📦 **Naya Product Request** from `{client_id}`")
            st.write(f"**Details:** {order_data['msg']}")
            
            ceo_price = st.text_input(f"Iska price set karein (₹):", key=f"p_{client_id}")
            if st.button(f"Confirm Price & Send", key=f"btn_{client_id}"):
                if ceo_price:
                    st.session_state.orders[client_id]['status'] = 'price_sent'
                    url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
                    reply = f"Amit here! CEO Sir ne is product ka price ₹{ceo_price} confirm kar diya hai."
                    requests.post(url, json={"chatId": client_id, "message": reply})
                    st.success("Price bhej diya gaya!")
                    del st.session_state.orders[client_id]
                    st.rerun()

with col2:
    st.header("🧮 C.A. Sharma Ji")
    st.info("Deals poori hone par Sharma Ji yahan bill banayenge.")

st.write("---")
if st.button("🔄 Force Check WhatsApp Messages"):
    st.rerun()
