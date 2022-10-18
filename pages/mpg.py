from this import d
from turtle import title
from folium import Tooltip
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
import plotly.express as px
import altair as alt

st.set_page_config(
    page_title="Likelion AI School 자동차 연비 App",
    page_icon="🚗",
    layout="wide",
)

st.markdown("# 자동차 연비🚗")
st.sidebar.markdown("# 자동차 연비🚗")

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
data = pd.read_csv(url)

@st.cache
def load_data():
    data = pd.read_csv(url)
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache)")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year',
    list(reversed(range(data.model_year.min(),data.model_year.max())))
    )

if selected_year > 0 :
    data = data[data.model_year == selected_year]

# Sidebar - origin
sorted_unique_origin = sorted(data.origin.unique())
selected_origin = st.sidebar.multiselect('origin', sorted_unique_origin, sorted_unique_origin)

if len(selected_origin) > 0:
    data = data[data.origin.isin(selected_origin)]


st.dataframe(data)

st.line_chart(data["mpg"])

st.bar_chart(data["mpg"])

fig, ax = plt.subplots(figsize=(10, 3))
sns.countplot(data=data, x='origin').set_title("origin 별 자동차 연비")

st.pyplot(fig)

pxh = px.histogram(data, x='origin', title="지역별 자동차 연비 데이터 수")
st.plotly_chart(pxh)

c = alt.Chart(data).mark_circle().encode(x='mpg', y='weight', color='origin', 
    tooltip=['weight', 'origin']).properties(title="지역별 mpg에 따른 weight 관계")

st.altair_chart(c, use_container_width=True)

a = alt.Chart(data).mark_circle().encode(x='weight', y='horsepower', color='cylinders'
    ).properties(title="cylinder별 무게에 따른 마력의 관계")

st.altair_chart(a, use_container_width=True)

