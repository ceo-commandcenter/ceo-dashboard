import streamlit as st
import requests
import google.generativeai as genai

# Streamlit Secrets se saari keys load karna
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
GREEN_API_INSTANCE = st.secrets.get("GREEN_API_INSTANCE", "")
GREEN_API_TOKEN = st.secrets.get("GREEN_API_TOKEN", "")

# Gemini AI Configure karna
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

st.title("💼 CEO Command Center Dashboard")
st.write("🚀 WhatsApp AI Bot is actively running in the background...")

---

# 🤖 STEP 1: Dashboard par Teeno Agents ka Setup
st.subheader("👥 Select Active AI Agent")

agent_choice = st.radio(
    "Aap kis agent se WhatsApp handle karwana chahte hain?",
    ["Sharma Ji (Accountant & Sales Expert)", "Amit (Customer Support)", "Rohan (Tech Support & Aggressive Sales)"]
)

# Har agent ka alag dimaag (System Prompt)
if "Sharma Ji" in agent_choice:
    system_instruction = "Aapka naam Sharma Ji hai. Aap ek bohot hi anubhavi, thode shant aur baniya buddhi wale Indian accountant/salesman hain. Hamesha tameez se baat karte hain, beech-beech mein 'Beta', 'Bhai sahab' ya 'Arey' use karte hain aur har baat mein fayda/munafa dekhte hain. Hindi-English mix bhasha mein baat karein."
    st.success("👨‍💼 **Sharma Ji** abhi WhatsApp sambhal rahe hain!")
elif "Amit" in agent_choice:
    system_instruction = "Aapka naam Amit hai. Aap ek bohot hi polite, professional aur madadgar customer support executive hain. Aap customer ki har problem ko dhyan se sunte hain aur hamesha 'Sir/Ma'am' kehkar izzat se baat karte hain. Aapka maksad customer ko khush rakhna hai."
    st.success("🧑‍💼 **Amit** abhi WhatsApp sambhal rahe hain!")
else:
    system_instruction = "Aapka naam Rohan hai. Aap ek young, energetic tech support engineer aur thode aggressive salesman hain. Aap bohot fast baat karte hain, modern slang (bro, dude, cool) use karte hain, aur customer ko jaldi se tech solve karke product bechne ki koshish karte hain."
    st.success("🧑‍💻 **Rohan** abhi WhatsApp sambhal rahe hain!")

---

# 📲 STEP 2: Green API se Real-time WhatsApp Messages Check Karna
if GREEN_API_INSTANCE and GREEN_API_TOKEN:
    try:
        receive_url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/receiveNotification/{GREEN_API_TOKEN}"
        response = requests.get(receive_url, timeout=5).json()
        
        if response and "receiptId" in response:
            receipt_id = response["receiptId"]
            body = response.get("body", {})
            
            # Agar koi text message aaya hai
            if body.get("typeWebhook") == "incomingMessageReceived":
                message_data = body.get("messageData", {})
                text_message_data = message_data.get("textMessageData", {})
                user_msg = text_message_data.get("textMessage", "")
                sender_id = body.get("senderData", {}).get("chatId", "")
                
                if user_msg and sender_id:
                    print(f"--- Naya Message Aaya: {user_msg} ---")
                    
                    # Gemini AI se Selected Agent ki personality ke sath reply taiyar karna
                    model = genai.GenerativeModel(
                        model_name='gemini-pro',
                        generation_config={"temperature": 0.7}
                    )
                    
                    # Selected Agent ki prompt ke sath user ka message jodna
                    full_prompt = f"{system_instruction}\n\nCustomer ne kaha: '{user_msg}'\nAb iska upar batayi personality ke mutabik ek badhiya sa jawab do:"
                    
                    ai_response = model.generate_content(full_prompt)
                    ai_reply = ai_response.text
                    
                    # Reply ko wapas WhatsApp par bhej dena
                    send_url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
                    payload = {"chatId": sender_id, "message": ai_reply}
                    requests.post(send_url, json=payload)
                    print(f"--- Reply Bhej Diya ({agent_choice}): {ai_reply} ---")
            
            # Notification ko delete karna taaki repeat na ho
            delete_url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/deleteNotification/{GREEN_API_TOKEN}/{receipt_id}"
            requests.delete(delete_url)
            st.rerun()
            
    except Exception as e:
        print(f"Error checking message: {e}")

# Live monitoring widget on UI
st.subheader("📊 System Status")
st.info("Bot WhatsApp server se connected hai aur naye messages ka wait kar raha hai.")
