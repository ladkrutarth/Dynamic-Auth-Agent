import streamlit as st
import pandas as pd
import time
import datetime
import os
import csv

# --- CONFIGURATION & SETUP ---
st.set_page_config(page_title="GraphGuard Auditor", layout="wide")
LOG_FILE = "logs/product_metrics.csv"

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Initialize Log File if missing
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Query", "Latency_Seconds", "Evidence_Source", "Status"])

# --- MOCK RAG ENGINE (For UI Demo Stability) ---
# NOTE: In a real deployment, you import your 'rag_chain' from Week 3 here.
# We simulate the response to ensure the UI/Logging works perfectly for your screenshot.
def query_graphguard_compliance(user_query):
    start_time = time.time()
    
    # Simulation logic based on keywords
    if "AAL3" in user_query or "requirements" in user_query:
        response = "According to NIST SP 800-63B (Table 5-1), AAL3 requires a **hardware-based authenticator** and cryptographic resistance to verifier impersonation."
        evidence = "nist_guidelines.pdf (Page 42), aal_table.png (Chart)"
        status = "Success"
    elif "password" in user_query:
        response = "Passwords must be salted and hashed using a suitable one-way key derivation function (NIST SP 800-63B, Section 5.1.1.2)."
        evidence = "nist_guidelines.pdf (Page 18)"
        status = "Success"
    elif "cake" in user_query:
        response = "I cannot answer this as it is not in the provided banking policy documents."
        evidence = "None"
        status = "Refusal"
    else:
        response = "Based on the provided context, I found relevant guidelines regarding identity proofing."
        evidence = "nist_guidelines.pdf (General Context)"
        status = "Success"
        
    latency = round(time.time() - start_time, 4)
    return response, evidence, latency, status

# --- SIDEBAR: METRICS PANEL ---
st.sidebar.title("📊 System Health")
st.sidebar.markdown("---")

# Load Logs for Dashboard
if os.path.exists(LOG_FILE):
    df = pd.read_csv(LOG_FILE)
    if not df.empty:
        avg_latency = df["Latency_Seconds"].mean()
        total_queries = len(df)
        st.sidebar.metric("Total Audits", total_queries)
        st.sidebar.metric("Avg Latency", f"{avg_latency:.3f}s")
        st.sidebar.dataframe(df.tail(5)) # Show last 5 logs
    else:
        st.sidebar.info("No logs yet.")

# --- MAIN INTERFACE ---
st.title("🛡️ GraphGuard Compliance Auditor")
st.markdown("### Internal Audit Tool for Identity Verification Policies")
st.info("Use this tool to verify if dynamic security questions comply with NIST 800-63B.")

# Query Input
query = st.text_input("Enter Compliance Question:", placeholder="e.g., What are the requirements for AAL3?")

if st.button("Run Audit"):
    if query:
        with st.spinner("Analyzing NIST Guidelines..."):
            # 1. Run Logic
            answer, evidence, latency, status = query_graphguard_compliance(query)
            
            # 2. Log Interaction
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(LOG_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, query, latency, evidence, status])
            
            # 3. Display Result
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("📝 Audit Finding")
                st.success(answer)
            
            with col2:
                st.subheader("🔍 Evidence Pack")
                st.warning(f"**Source:** {evidence}")
                st.caption(f"Latency: {latency}s | Status: {status}")
                
            # Refresh to update sidebar metrics
            st.rerun()
    else:
        st.error("Please enter a query.")

# --- FOOTER ---
st.markdown("---")
st.caption("GraphGuard Capstone | Week 4 Integration Sprint")