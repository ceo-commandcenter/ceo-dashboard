import streamlit as st

# Page Configuration (CEO Dashboard Theme)
st.set_page_config(page_title="CEO Control Room", page_icon="👑", layout="wide")

# Top Title Banner
st.title("👑 CEO COMMAND CENTER")
st.subheader("Welcome Back, CEO! Track your AI Agents Live.")
st.markdown("---")

# Sidebar for Agent Selection with Indian Names in brackets
st.sidebar.header("📁 AGENT DEPARTMENTS")
selected_agent = st.sidebar.radio(
    "Choose an agent to audit:",
    ["📢 Marketing Manager (Rohan)", "💰 Sales Executive (Amit)", "📑 CA (Sharma Ji)"]
)

# --- 1. MARKETING MANAGER (ROHAN) ---
if selected_agent == "📢 Marketing Manager (Rohan)":
    st.header("📢 Marketing Department — Managed by Rohan")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Leads Generated", value="1,240", delta="+120 Today")
    col2.metric(label="Ad Campaign Budget", value="₹15,000", delta="-₹2,000 Spent")
    col3.metric(label="Conversion Rate", value="4.2%", delta="+0.5%")
    
    st.subheader("📄 Live Strategy & Ads Log")
    st.info("Rohan: Running target ads for retail clients in Delhi NCR. High engagement noticed on Instagram posts.")

# --- 2. SALES EXECUTIVE (AMIT) WITH MULTI-PLATFORM CHATS ---
elif selected_agent == "💰 Sales Executive (Amit)":
    st.header("💰 Sales Department — Managed by Amit")
    
    # Sales Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Deals Closed Today", value="14 Deals", delta="+4 vs Yesterday")
    col2.metric(label="Pipeline Value", value="₹4,50,000", delta="+₹50,000")
    col3.metric(label="Active Lead Channels", value="3 Platforms", delta="WhatsApp, Email, LinkedIn")
    
    st.subheader("📱 Omnichannel Buyer Communication Audit")
    st.write("Select a platform below to see the live chats and interactions Amit is having with buyers:")
    
    # Creating Tabs for WhatsApp, Email, and LinkedIn
    tab_whatsapp, tab_email, tab_linkedin = st.tabs(["🟢 WhatsApp Chats", "📧 Email Outreach", "🔵 LinkedIn Conversations"])
    
    with tab_whatsapp:
        st.subheader("🟢 Live WhatsApp Chat Screen (Dedicated Business Number)")
        st.success("**Amit (Sales Agent) -> Client (Rahul Kumar):**\n\n'Namaste Rahul ji! Thanks for showing interest. Standard pricing is ₹50,000, but since you are our premium member, I can lock this deal at a 10% discount if you complete the 10% advance payment today. Sharing the secure payment link now.'")
        st.text_area("Live WhatsApp Logs (Incoming Responses):", value="[10:42 PM] Buyer Rahul Kumar: Link bhejo, main abhi advance transfer karta hoon.\n[10:45 PM] Amit: Link shared. Waiting for confirmation.", height=100, disabled=True)
        
    with tab_email:
        st.subheader("📧 Sent & Received Emails")
        st.info("**Subject:** Proposal for Enterprise Automation Solution\n\n**To:** director@techcorp.in\n\n'Dear Sir, Following up on our call, I have attached the customized quotation for your review. Our team can initiate deployment by this weekend. Looking forward to your approval.'\n\n*Regards,\nAmit (Sales Executive)*")
        
    with tab_linkedin:
        st.subheader("🔵 LinkedIn InMail Conversations")
        st.warning("**Amit (InMail Bot) -> Prospect (Neha Sharma, HR Head):**\n\n'Hi Neha, love your insights on remote work culture! I noticed your team is expanding rapidly. We recently helped a similar company automate 40% of their operations. Would love to drop a quick 5-minute video presentation if you're open to it?'")

# --- 3. CA (SHARMA JI) ---
elif selected_agent == "📑 CA (Sharma Ji)":
    st.header("📑 Finance & Accounts Department — Managed by Sharma Ji")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Revenue", value="₹8,20,000", delta="+₹1,10,000 This Month")
    col2.metric(label="Pending Invoices", value="3 Bills", delta="Urgent Alert", delta_color="inverse")
    col3.metric(label="Tax Liability (Est.)", value="₹45,000", delta="Safe Limit")
    
    st.subheader("📋 Ledger & Bill Verification Log")
    st.warning("Sharma Ji: Verifying Ledger for Client #1092. GST calculation is complete. Awaiting CEO approval for final filing.")