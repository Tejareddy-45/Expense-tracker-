import streamlit as st
import json
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
