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


df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()
st.sidebar.header("Choose your filter:")

#  With region filter
region = st.sidebar.multiselect("Pick your region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# State Filter
state = st.sidebar.multiselect("Pick your state", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

# City Filter
city = st.sidebar.multiselect("Pick your city", df3["City"].unique())

if not region and not state and not city:
    filtered_df = df
elif not state and not state:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[
        df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)
    ]

category_df = filtered_df.groupby(by=["Category"], as_index=False)["Sales"].sum()
with col1:
    st.subheader("Category Wise Sales")
    fig = px.bar(
        category_df,
        x="Category",
        y="Sales",
        text=[f"${x:,.2f}" for x in category_df["Sales"]],
        template="seaborn",
    )
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("Region Wise Sales")
    fig = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
    fig.update_traces(text=filtered_df["Region"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
