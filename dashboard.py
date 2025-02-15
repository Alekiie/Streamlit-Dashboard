import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings

warnings.filterwarnings("ignore")
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")
st.title(" :bar_chart: Sales Dashboard")
st.markdown(
    "<style>div.block-container{padding-top:2rem;} </style>", unsafe_allow_html=True
)

# File uploader
fl = st.file_uploader(
    " :file_folder: Please upload a file", type=(["csv", "xlsx", "xls", "txt"])
)


# Function to read the file
def read_file(file_path):
    if file_path.endswith(".csv") or file_path.endswith(".txt"):
        return pd.read_csv(file_path, encoding="ISO-8859-1")
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        return pd.read_excel(file_path)
    else:
        st.error("Unsupported file format")
        return None


# Check if file is uploaded
if fl is not None:
    filename = fl.name
    st.write("Uploaded file:", filename)
    df = read_file(fl)
else:
    os.chdir("/home/alexander/projects/Python/streamlit-proj")
    df = read_file("Sample - Superstore.xls")

# Display the data
if df is not None:
    st.dataframe(df.head())


col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))
