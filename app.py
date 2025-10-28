import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="💸 Finance Tracker", layout="centered")

st.title("💸 Personal Finance Tracker")

# CSV storage file
DATA_FILE = "expenses.csv"

# Initialize CSV if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Expense Name", "Amount", "Category"])
    df.to_csv(DATA_FILE, index=False)

# Load existing data
df = pd.read_csv(DATA_FILE)

# ---- Input Section ----
st.header("➕ Add New Expense")

expense_name = st.text_input("Expense Name")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
category = st.selectbox(
    "Category",
    ["🍇 Food", "👔 Clothes", "📲 SIM Card", "📺 Entertainment", "💸 Debts", "✨ Misc"]
)

if st.button("Add Expense"):
    if expense_name and amount > 0:
        new_entry = pd.DataFrame(
            {"Expense Name": [expense_name], "Amount": [amount], "Category": [category]}
        )
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Added '{expense_name}' to {category} for ₹{amount:.2f}")
    else:
        st.error("Please fill all fields correctly.")

# ---- Display Section ----
st.header("📊 Expense Summary")

if not df.empty:
    st.dataframe(df, hide_index=True)

    total_spent = df["Amount"].sum()
    st.metric("Total Spent", f"₹{total_spent:,.2f}")

    category_summary = df.groupby("Category")["Amount"].sum().reset_index()
    st.bar_chart(category_summary.set_index("Category"))

    if st.button("Clear All Data ⚠️"):
        df = pd.DataFrame(columns=["Expense Name", "Amount", "Category"])
        df.to_csv(DATA_FILE, index=False)
        st.warning("All expenses cleared!")
else:
    st.info("No expenses recorded yet.")
