# Sidebar - Agent Selection (Sharmaji wapas aa gaye!)
st.sidebar.title("📁 AGENT DEPARTMENTS")
agent = st.sidebar.radio("Choose an agent to audit:", ["📢 Marketing Manager (Rohan)", "💼 Sales Executive (Amit)", "📊 Sharmaji (CA - Finance)"])

# ... (baaki code waisa hi rehne dein) ...

# Main Dashboard Screen mein yeh naya section add kijiye:
elif agent == "📊 Sharmaji (CA - Finance)":
    st.header("📊 Finance Department — Managed by Sharmaji (CA)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Balance", "₹12,40,000", "+₹50,000")
    col2.metric("Tax Liability", "₹85,000", "Due: 15th June")
    col3.metric("Profit Margin", "22%", "+2%")
    
    st.subheader("🤖 Ask Sharmaji for Financial Advice")
    user_input = st.text_input("Sharmaji ko hisab-kitab ka order dijiye:")
    if st.button("Generate Report"):
        st.info(f"Sharmaji file dekh rahe hain '{user_input}'... unka jawab jald hi aayega!")
