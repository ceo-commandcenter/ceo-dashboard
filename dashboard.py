import streamlit as st
import requests
import google.generativeai as genai

# Streamlit Secrets se keys load karna
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GREEN_API_INSTANCE = st.secrets["GREEN_API_INSTANCE"]
GREEN_API_TOKEN = st.secrets["GREEN_API_TOKEN"]

# Gemini AI ko configure karna
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.title("CEO Command Center Dashboard")
st.write("WhatsApp AI Bot is running...")

# Green API se webhook notification receive karne ka endpoint
# (Agar aapka framework FastAPI/Flask handles karta hai toh use wahi rehne dein, 
# yeh ek basic handler hai jo chat handle karega)

def handle_whatsapp_message(text, sender_id):
    try:
        # Gemini AI se reply generate karna
        response = model.generate_content(text)
        ai_reply = response.text
        
        # Green API ke zariye reply wapas bhejna
        url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
        payload = {
            "chatId": sender_id,
            "message": ai_reply
        }
        headers = {'Content-Type': 'application/json'}
        requests.post(url, json=payload, headers=headers)
    except Exception as e:
        print(f"Error: {e}")
