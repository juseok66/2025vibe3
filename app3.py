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

# 범죄유형 선택
범죄유형_list = df_melted["범죄유형"].unique()
selected_type = st.selectbox("범죄유형을 선택하세요", 범죄유형_list)

# 선택된 유형 필터링
df_filtered = df_melted[df_melted["범죄유형"] == selected_type]

# Plotly 시각화
fig = px.line(df_filtered, x="연도", y="범죄율", title=f"연도별 {selected_type} 범죄율 추이",
              markers=True)
fig.update_layout(xaxis_title="연도", yaxis_title="범죄율 (인구 10만 명당)")
st.plotly_chart(fig)

