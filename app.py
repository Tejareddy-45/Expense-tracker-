import streamlit as st
import json
import os

# File to store data
FILE_NAME = "expenses.json"

# Load expenses
def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# Save expenses
def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file)

# Initialize
expenses = load_expenses()

st.title("💰 Expense Tracker")

# Add Expense
st.header("➕ Add New Expense")
name = st.text_input("Expense Name")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")

if st.button("Add Expense"):
    if name and amount > 0:
        expenses.append({"name": name, "amount": amount})
        save_expenses(expenses)
        st.success("Expense added successfully!")
    else:
        st.error("Please enter valid details")

# Show Expenses
st.header("📋 All Expenses")
if expenses:
    total = 0
    for exp in expenses:
        st.write(f"{exp['name']} - ₹{exp['amount']}")
        total += exp['amount']
    
    st.subheader(f"💵 Total Spending: ₹{total}")
else:
    st.write("No expenses yet.")

# Clear Data
if st.button("🗑 Clear All Expenses"):
    save_expenses([])
    st.warning("All expenses cleared!")
