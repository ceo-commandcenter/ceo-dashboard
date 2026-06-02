import streamlit as st

# Streamlit ki tijori se sirf Password uthana
try:
    CORRECT_PASSWORD = st.secrets["APP_PASSWORD"]
except:
    CORRECT_PASSWORD = "admin" # Backup password agar secrets set na ho

st.set_page_config(page_title="CEO Control Room", page_icon="👑", layout="wide")

# --- PASSWORD LOCK SCREEN ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 Security Access Required")
    st.subheader("CEO Dashboard is encrypted. Please enter your Master Key.")
    
    user_password = st.text_input("Enter Master Key / Password:", type="password")
    if st.button("Unlock Dashboard"):
        if user_password == CORRECT_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ Invalid Key! Access Denied.")
    st.stop()

# --- AGAR PASSWORD SAHI HAI TOH YEH DIKHEGA ---
st.title("👑 CEO COMMAND CENTER")
st.subheader("Welcome Back, CEO! Track and Command your AI Agents Live.")

# Sidebar - Agent Selection
st.sidebar.title("📁 AGENT DEPARTMENTS")
agent = st.sidebar.radio("Choose an agent to audit:", ["📢 Marketing Manager (Rohan)", "💼 Sales Executive (Amit)"])

if st.sidebar.button("🔒 Lock Dashboard (Logout)"):
    st.session_state["authenticated"] = False
    st.rerun()

# Main Dashboard Screen
if agent == "📢 Marketing Manager (Rohan)":
    st.header("📢 Marketing Department — Managed by Rohan")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Leads Generated", "1,240", "+120 Today")
    col2.metric("Ad Campaign Budget", "₹15,000", "-₹2,000 Spent")
    col3.metric("Conversion Rate", "4.2%", "+0.5%")
    
    st.subheader("🤖 Ask Rohan for a Marketing Strategy")
    user_input = st.text_input("Rohan ko order dijiye:")
    if st.button("Generate Strategy"):
        st.info(f"Rohan aapke order '{user_input}' par kaam kar raha hai! (AI key connect hote hi live reply aane lagega).")

elif agent == "💼 Sales Executive (Amit)":
    st.header("💼 Sales Department — Managed by Amit")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales Done", "₹4,50,000", "+₹45,000 Today")
    col2.metric("Pending Deals", "18 Deals", "-2 Closed")
    col3.metric("Target Achieved", "78%", "+5% This Week")

    st.subheader("🤖 Ask Amit for a Sales Pitch")
    user_input = st.text_input("Amit ko order dijiye:")
    if st.button("Get Pitch"):
        st.info(f"Amit aapke order '{user_input}' ke liye pitch taiyar kar raha hai! (AI key connect hote hi live reply aane lagega).")
