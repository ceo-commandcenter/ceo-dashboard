import streamlit as st
import requests
import google.generativeai as genai

# Keys setup
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
GREEN_API_INSTANCE = st.secrets.get("GREEN_API_INSTANCE", "")
GREEN_API_TOKEN = st.secrets.get("GREEN_API_TOKEN", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

st.title("💼 CEO Command Center: AI Empire")

# Session state management
if "orders" not in st.session_state: st.session_state.orders = {}
if "leads" not in st.session_state: st.session_state.leads = []

# --- 1. MARKETING MANAGER (ROHAN) ---
st.subheader("📢 Marketing Manager (Rohan)")
if st.button("Rohan: Find Indian Handicraft Buyers"):
    model = genai.GenerativeModel('gemini-pro')
    res = model.generate_content("Find potential buyers for Indian handicrafts and generate a lead list with phone numbers.")
    st.session_state.leads.append(res.text)
    st.write("Leads generated and passed to Amit!")

# --- 2. SALES MANAGER (AMIT) ---
st.subheader("🤝 Sales Manager (Amit)")
# Dashboard Price Input
order_id = st.text_input("Enter Order ID for Price Update:")
price = st.text_input("Set Price for Client:")
if st.button("Confirm Price & Notify Client"):
    if order_id in st.session_state.orders:
        client_id = st.session_state.orders[order_id]['client']
        url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
        requests.post(url, json={"chatId": client_id, "message": f"CEO Sir ne aapke order ka price ₹{price} confirm kiya hai."})
        st.success("Price sent to client!")

# --- 3. C.A. SHARMA JI ---
st.subheader("🧮 C.A. Sharma Ji")
if st.button("Generate Profit Report & Bill"):
    model = genai.GenerativeModel('gemini-pro')
    report = model.generate_content("Calculate profit based on current orders and generate a professional invoice.")
    st.write(report.text)

# --- WHATSAPP LOGIC (Brief) ---
st.info("Bots are actively monitoring WhatsApp...")
# (Yahan aapka purana logic rahega jo message incoming track karega)
