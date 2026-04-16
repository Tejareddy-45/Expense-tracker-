import streamlit as st
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page config
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# Title
st.title("💰 Advanced Expense Tracker")

# File to store data
FILE = "expenses.csv"

# Load data
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["Name", "Amount", "Category", "Date"])

# Sidebar
st.sidebar.header("📌 Menu")
menu = st.sidebar.radio("Go to", ["Add Expense", "View Expenses"])

# Add Expense
if menu == "Add Expense":
    st.subheader("➕ Add New Expense")

    name = st.text_input("Expense Name")
    amount = st.number_input("Amount", min_value=0.0)
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Other"])
    date = st.date_input("Date", datetime.now())

    if st.button("Add Expense"):
        new_data = pd.DataFrame({
            "Name": [name],
            "Amount": [amount],
            "Category": [category],
            "Date": [date]
        })

        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(FILE, index=False)

        st.success("✅ Expense added successfully!")

# View Expenses
elif menu == "View Expenses":
    st.subheader("📊 All Expenses")

    if not df.empty:
        st.dataframe(df)

        total = df["Amount"].sum()
        st.markdown(f"## 💸 Total Spending: ₹{total}")

        st.subheader("📊 Category-wise Spending")
        chart_data = df.groupby("Category")["Amount"].sum()
        st.bar_chart(chart_data)

        # Delete option
        st.subheader("🗑️ Delete Expense")
        index = st.number_input("Enter index to delete", min_value=0, max_value=len(df)-1, step=1)

        if st.button("Delete"):
            df = df.drop(index)
            df.to_csv(FILE, index=False)
            st.success("Deleted successfully! Refresh page.")

    else:
        st.info("No expenses yet!") json
import os

FILE_NAME = "expenses.json"

def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)

expenses = load_expenses()

st.title("💰 Expense Tracker")

st.subheader("Add Expense")
name = st.text_input("Expense Name")
amount = st.number_input("Amount", min_value=0.0)

if st.button("Add Expense"):
    if name:
        expenses.append({"name": name, "amount": amount})
        save_expenses(expenses)
        st.success("✅ Expense added!")
    else:
        st.error("❌ Enter expense name")

st.subheader("All Expenses")
for exp in expenses:
    st.write(f"{exp['name']} - ₹{exp['amount']}")

total = sum(exp["amount"] for exp in expenses)
st.subheader(f"Total Spending: ₹{total}")
