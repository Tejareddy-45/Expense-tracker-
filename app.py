import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("📊 Personal Expense Tracker")

# Initialize session state for data persistence during the session
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Description", "Amount", "Category"])

# Sidebar for Input
st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form", clear_on_submit=True):
    desc = st.text_input("Description")
    amt = st.number_input("Amount", min_value=0.0, step=0.01)
    cat = st.selectbox("Category", ["Food", "Transport", "Tech", "Utilities", "Other"])
    submit = st.form_submit_button("Add Expense")

    if submit and desc:
        new_data = pd.DataFrame([[desc, amt, cat]], columns=["Description", "Amount", "Category"])
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_data], ignore_index=True)

# Main Dashboard
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Transaction History")
    if not st.session_state.expenses.empty:
        st.dataframe(st.session_state.expenses, use_container_width=True)
    else:
        st.info("No expenses recorded yet.")

with col2:
    st.subheader("Summary")
    if not st.session_state.expenses.empty:
        total = st.session_state.expenses["Amount"].sum()
        st.metric("Total Spent", f"${total:,.2f}")
        
        # Categorical Breakdown
        chart_data = st.session_state.expenses.groupby("Category")["Amount"].sum()
        st.pie_chart(chart_data)
    else:
        st.write("Add expenses to see the breakdown.")

# Option to clear data
if st.button("Clear All Data"):
    st.session_state.expenses = pd.DataFrame(columns=["Description", "Amount", "Category"])
    st.rerun()
import pandas as pd
from datetime import datetime
import os

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

FILE = "expenses.csv"

# ------------------ LOAD DATA ------------------
def load_data():
    if os.path.exists(FILE):
        try:
            return pd.read_csv(FILE)
        except:
            return pd.DataFrame(columns=["Name", "Amount", "Category", "Date"])
    else:
        return pd.DataFrame(columns=["Name", "Amount", "Category", "Date"])

# ------------------ SAVE DATA ------------------
def save_data(df):
    df.to_csv(FILE, index=False)

# ------------------ LOGIN ------------------
def login():
    st.title("🔐 Login")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# ------------------ MAIN APP ------------------
st.title("💰 Expense Tracker Dashboard")

df = load_data()

# Sidebar
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio(
    "Navigate",
    ["Add Expense", "View Expenses", "Download Report", "Logout"],
    key="menu_radio"
)

# ------------------ ADD EXPENSE ------------------
if menu == "Add Expense":
    st.subheader("➕ Add Expense")

    name = st.text_input("Expense Name", key="name_input")
    amount = st.number_input("Amount", min_value=0.0, key="amount_input")
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Other"],
        key="category_input"
    )
    date = st.date_input("Date", datetime.now(), key="date_input")

    if st.button("Add Expense", key="add_btn"):
        if name and amount > 0:
            new_row = pd.DataFrame({
                "Name": [name],
                "Amount": [amount],
                "Category": [category],
                "Date": [date]
            })

            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)

            st.success("✅ Expense Added!")
        else:
            st.warning("Please enter valid data")

# ------------------ VIEW EXPENSES ------------------
elif menu == "View Expenses":
    st.subheader("📊 All Expenses")

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        total = df["Amount"].sum()
        st.markdown(f"## 💸 Total Spending: ₹{total}")

        st.subheader("📊 Category-wise Spending")
        chart = df.groupby("Category")["Amount"].sum()
        st.bar_chart(chart)

        # Delete option
        st.subheader("🗑️ Delete Expense")
        index = st.number_input(
            "Enter index to delete",
            min_value=0,
            max_value=len(df)-1,
            step=1,
            key="delete_index"
        )

        if st.button("Delete", key="delete_btn"):
            df = df.drop(index).reset_index(drop=True)
            save_data(df)
            st.success("Deleted successfully! Refresh page.")

    else:
        st.info("No expenses yet!")

# ------------------ DOWNLOAD ------------------
elif menu == "Download Report":
    st.subheader("📥 Download Your Data")

    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="expenses.csv",
            mime="text/csv",
            key="download_btn"
        )
    else:
        st.warning("No data to download!")

# ------------------ LOGOUT ------------------
elif menu == "Logout":
    st.session_state.logged_in = False
    st.success("Logged out! Please refresh.") 
import pandas as pd
from datetime import datetime
import os

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

FILE = "expenses.csv"

# ------------------ LOAD DATA ------------------
def load_data():
    if os.path.exists(FILE):
        try:
            return pd.read_csv(FILE)
        except:
            return pd.DataFrame(columns=["Name", "Amount", "Category", "Date"])
    else:
        return pd.DataFrame(columns=["Name", "Amount", "Category", "Date"])

# ------------------ SAVE DATA ------------------
def save_data(df):
    df.to_csv(FILE, index=False)

# ------------------ LOGIN ------------------
def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# ------------------ MAIN APP ------------------
st.title("💰 Expense Tracker Dashboard")

df = load_data()

# Sidebar
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio("Navigate", ["Add Expense", "View Expenses", "Download Report", "Logout"])

# ------------------ ADD EXPENSE ------------------
if menu == "Add Expense":
    st.subheader("➕ Add Expense")

    name = st.text_input("Expense Name")
    amount = st.number_input("Amount", min_value=0.0)
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Other"])
    date = st.date_input("Date", datetime.now())

    if st.button("Add Expense"):
        if name and amount > 0:
            new_row = pd.DataFrame({
                "Name": [name],
                "Amount": [amount],
                "Category": [category],
                "Date": [date]
            })

            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)

            st.success("✅ Expense Added!")
        else:
            st.warning("Please enter valid data")

# ------------------ VIEW EXPENSES ------------------
elif menu == "View Expenses":
    st.subheader("📊 All Expenses")

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        total = df["Amount"].sum()
        st.markdown(f"## 💸 Total Spending: ₹{total}")

        st.subheader("📊 Category-wise Spending")
        chart = df.groupby("Category")["Amount"].sum()
        st.bar_chart(chart)

        # Delete option
        st.subheader("🗑️ Delete Expense")
        index = st.number_input("Enter index to delete", min_value=0, max_value=len(df)-1, step=1)

        if st.button("Delete"):
            df = df.drop(index).reset_index(drop=True)
            save_data(df)
            st.success("Deleted successfully! Refresh page.")

    else:
        st.info("No expenses yet!")

# ------------------ DOWNLOAD ------------------
elif menu == "Download Report":
    st.subheader("📥 Download Your Data")

    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="expenses.csv",
            mime="text/csv",
        )
    else:
        st.warning("No data to download!")

# ------------------ LOGOUT ------------------
elif menu == "Logout":
    st.session_state.logged_in = False
    st.success("Logged out! Please refresh.")
import pandas as pd
import json
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
        st.info("No expenses yet!")
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
