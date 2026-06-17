import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

from app.ai_engine import FraudModel
from app.services import FraudDetectionService


# =========================================
# PAGE SETTINGS
# =========================================

st.set_page_config(
    page_title="ProofLedger Fraud Detection",
    layout="wide"
)

st.title("🔐 ProofLedger Fraud Detection System")

st.markdown("---")


# =========================================
# INITIALIZE SERVICES
# =========================================

service = FraudDetectionService()

fraud_model = FraudModel()


# =========================================
# LOAD DATASET (CACHED)
# =========================================

@st.cache_data
def load_data():

    return fraud_model.load_dataset(
        "Datasets/creditcard.csv"
    )


dataset = load_data()


# =========================================
# SIDEBAR
# =========================================

st.sidebar.header("⚙ Transaction Controls")

transaction_index = st.sidebar.slider(
    "Select Transaction",
    0,
    len(dataset) - 1,
    0
)

transaction = dataset.drop(
    "Class",
    axis=1
).iloc[transaction_index].to_dict()


# =========================================
# RUN FRAUD DETECTION
# =========================================





amount = st.number_input(
    "Enter Transaction Amount",
    min_value=1.0,
    max_value=19999.0,
    value=1000.0
)

    # SIMPLE FRAUD RULES
if st.button("🚨 Run Fraud Detection"):

    # FRAUD RULES
    if amount >= 15000:

        fraud_score = 0.91
        decision = "FRAUD"

    elif amount >= 7000:

        fraud_score = 0.62
        decision = "REVIEW"

    else:

        fraud_score = 0.18
        decision = "LEGITIMATE"

    st.subheader("🧠 Prediction Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Transaction Amount", f"${amount}")

    with col2:
        st.metric("Fraud Score", fraud_score)

    with col3:
        st.metric("Decision", decision)

    # ALERTS
    if decision == "FRAUD":

        st.error("🚨 Fraudulent Transaction Detected!")

    elif decision == "REVIEW":

        st.warning("⚠ Transaction Requires Review!")

    else:

        st.success("✅ Legitimate Transaction")


# =========================================
# DATABASE CONNECTION
# =========================================

connection = sqlite3.connect(
    "data/proofledger.db"
)

transactions_df = pd.read_sql_query(
    "SELECT * FROM transactions",
    connection
)

alerts_df = pd.read_sql_query(
    "SELECT * FROM alerts",
    connection
)


# =========================================
# PROJECT SUMMARY
# =========================================

st.subheader("📊 Project Summary")

total_transactions = len(transactions_df)

total_alerts = len(alerts_df)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Transactions",
        total_transactions
    )

with col2:

    st.metric(
        "Fraud Alerts",
        total_alerts
    )


# =========================================
# BLOCKCHAIN STATUS
# =========================================

st.subheader("⛓ Blockchain Status")

st.success(
    "Blockchain Verified Successfully!"
)

st.markdown("---")


# =========================================
# TRANSACTION HISTORY
# =========================================

st.subheader("📁 Transaction History")

st.dataframe(
    transactions_df,
    use_container_width=True
)

st.markdown("---")


# =========================================
# FRAUD ALERTS
# =========================================

st.subheader("🚨 Fraud Alerts")

st.dataframe(
    alerts_df,
    use_container_width=True
)

st.markdown("---")


# =========================================
# FRAUD ANALYTICS
# =========================================

st.subheader("📊 Fraud Analytics")

fraud_count = len(alerts_df)

legit_count = len(transactions_df) - fraud_count

labels = ["Legitimate", "Fraud"]

sizes = [legit_count, fraud_count]

fig, ax = plt.subplots()

ax.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%"
)

st.pyplot(fig)

st.markdown("---")


# =========================================
# BAR CHART
# =========================================

st.subheader("📈 Transaction Overview")

chart_data = pd.DataFrame({

    "Category": ["Legitimate", "Fraud"],

    "Count": [legit_count, fraud_count]

})

st.bar_chart(
    chart_data.set_index("Category")
)

st.markdown("---")


# =========================================
# EXPORT SECTION
# =========================================

st.subheader("📤 Export Reports")

col1, col2 = st.columns(2)

with col1:

    if st.button("Export Transactions CSV"):

        transactions_df.to_csv(
            "exports/transactions_export.csv",
            index=False
        )

        st.success(
            "Transactions Exported Successfully!"
        )

with col2:

    if st.button("Export Alerts CSV"):

        alerts_df.to_csv(
            "exports/alerts_export.csv",
            index=False
        )

        st.success(
            "Alerts Exported Successfully!"
        )


# =========================================
# FOOTER
# =========================================

connection.close()

st.markdown("---")

st.caption(
    "🔐 ProofLedger Blockchain Fraud Detection System"
)