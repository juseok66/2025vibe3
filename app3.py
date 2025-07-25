import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    xls = pd.ExcelFile("범죄율3.xlsx")
    df = xls.parse("범죄율2")
    df.columns = df.columns.astype(str)
    df = df.rename(columns={df.columns[0]: "범죄대분류", df.columns[1]: "범죄유형"})
    df.fillna(method='ffill', inplace=True)
    return df

df = load_data()

# 데이터 전처리
value_vars = [col for col in df.columns if col.isdigit()]
df_melted = df.melt(id_vars=["범죄대분류", "범죄유형"], value_vars=value_vars, 
                    var_name="연도", value_name="범죄율")
df_melted["연도"] = df_melted["연도"].astype(int)
df_melted.dropna(subset=["범죄율"], inplace=True)

# 페이지 설정
page = st.sidebar.radio("페이지 선택", ["전체 형법범죄", "주요 형법범죄"])

if page == "전체 형법범죄":
    st.header("전체 형법범죄 (막대 그래프)")
    df_total = df_melted[df_melted["범죄대분류"] == "전체\u00a0형법범죄"]
    fig_total = px.bar(df_total, x="연도", y="범죄율", title="전체 형법범죄 추이")
    fig_total.update_layout(xaxis_title="연도", yaxis_title="범죄율 (인구 10만 명당)")
    st.plotly_chart(fig_total)

if page == "주요 형법범죄":
    st.header("주요 형법범죄 (꺾은선 그래프)")
    범죄유형_list = df_melted[df_melted["범죄대분류"] == "주요\u00a0형법범죄"]["범죄유형"].unique()
    selected_types = st.multiselect("범죄유형을 선택하세요", 범죄유형_list, default=[범죄유형_list[0]])

    df_filtered = df_melted[(df_melted["범죄유형"].isin(selected_types)) & (df_melted["범죄대분류"] == "주요\u00a0형법범죄")]
    
    fig = px.line(df_filtered, x="연도", y="범죄율", color="범죄유형", title="주요 형법범죄별 연도별 추이", markers=True)
    fig.update_layout(xaxis_title="연도", yaxis_title="범죄율 (인구 10만 명당)")
    st.plotly_chart(fig)
