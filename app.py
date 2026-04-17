import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

FILE_NAME = "expenses.json"

# ------------------ Load डेटा ------------------
def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# ------------------ Save डेटा ------------------
def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file)

expenses = load_expenses()

st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💰 Advanced Expense Tracker")

# ------------------ Sidebar ------------------
st.sidebar.header("📂 Filters")

if expenses:
    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date'])

    min_date = df['date'].min()
    max_date = df['date'].max()

    start_date = st.sidebar.date_input("Start Date", min_date)
    end_date = st.sidebar.date_input("End Date", max_date)

    filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) &
                     (df['date'] <= pd.to_datetime(end_date))]
else:
    filtered_df = pd.DataFrame()

# ------------------ Add Expense ------------------
st.header("➕ Add Expense")

col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("Expense Name")

with col2:
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")

with col3:
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])

date = st.date_input("Date", datetime.today())

if st.button("Add Expense"):
    if name and amount > 0:
        expenses.append({
            "name": name,
            "amount": amount,
            "category": category,
            "date": str(date)
        })
        save_expenses(expenses)
        st.success("✅ Expense Added!")
        st.rerun()
    else:
        st.error("❌ Enter valid details")

# ------------------ Show Data ------------------
st.header("📋 Expense List")

if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)

    total = filtered_df['amount'].sum()
    st.subheader(f"💵 Total Spending: ₹{total:.2f}")

    # ------------------ Charts ------------------
    st.header("📊 Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Category-wise Spending")
        category_data = filtered_df.groupby("category")["amount"].sum()
        st.bar_chart(category_data)

    with col2:
        st.subheader("Daily Spending Trend")
        daily_data = filtered_df.groupby("date")["amount"].sum()
        st.line_chart(daily_data)

else:
    st.info("No expenses found for selected range.")

# ------------------ Delete Expense ------------------
st.header("🗑 Delete Expense")

if expenses:
    delete_index = st.number_input("Enter index to delete", min_value=0, max_value=len(expenses)-1, step=1)

    if st.button("Delete"):
        expenses.pop(delete_index)
        save_expenses(expenses)
        st.warning("Expense deleted!")
        st.rerun()

# ------------------ Clear All ------------------
if st.button("⚠️ Clear All Expenses"):
    save_expenses([])
    st.error("All data cleared!")
    st.rerun()
