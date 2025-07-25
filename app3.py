import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 연도별 범죄율 시각화")

# 1. 📁 엑셀 업로드
uploaded_file = st.file_uploader("범죄율 Excel 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    # 2. 엑셀 파일 읽기
    df = pd.read_excel(uploaded_file, sheet_name=0)

    # 3. 전처리
    df["범죄유형"] = df["Unnamed: 0"].fillna("") + df["Unnamed: 1"].fillna("")
    df = df.drop(columns=["Unnamed: 0", "Unnamed: 1"])
    df = df.set_index("범죄유형").T
    df.index.name = "연도"
    df = df.applymap(lambda x: str(x).replace(",", "").replace(".", "").replace("-", "").replace("없음", "").strip())
    df = df.apply(pd.to_numeric, errors="coerce")

    # 4. 긴 형식 변환
    df_long = df.reset_index().melt(id_vars="연도", var_name="범죄유형", value_name="범죄율")

    # 5. 시각화
    fig = px.line(df_long, x="연도", y="범죄율", color="범죄유형",
                  title="연도별 범죄율 변화",
                  labels={"연도": "Year", "범죄율": "Crime Rate"})
    fig.update_layout(legend_title_text="범죄 유형")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("왼쪽에서 범죄율 Excel 파일을 업로드해주세요.")
