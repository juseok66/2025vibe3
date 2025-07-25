import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 범죄율 분석 대시보드")

uploaded_file = st.file_uploader("📁 범죄율 Excel 파일 업로드 (.xlsx)", type=["xlsx"])

if uploaded_file:
    # 1. 엑셀 불러오기 및 전처리
    df = pd.read_excel(uploaded_file, sheet_name=0)
    df["범죄유형"] = df["Unnamed: 0"].fillna("") + df["Unnamed: 1"].fillna("")
    df = df.drop(columns=["Unnamed: 0", "Unnamed: 1"], errors="ignore")
    df = df.set_index("범죄유형").T
    df.index.name = "연도"
    df = df.applymap(lambda x: str(x).replace(",", "").replace(".", "").replace("-", "").replace("없음", "").strip())
    df = df.apply(pd.to_numeric, errors="coerce")
    df_long = df.reset_index().melt(id_vars="연도", var_name="범죄유형", value_name="범죄율")

    # 2. 범죄유형 분류
    전체_형법범죄 = [c for c in df.columns if "전체형법범죄" in c]
    주요_범죄들 = [c for c in df.columns if "주요형법범죄" in c and "전체" not in c]

    tab1, tab2 = st.tabs(["📌 전체 형법범죄", "📌 주요형법범죄 비교"])

    # ---------------- TAB 1 ----------------
    with tab1:
        st.subheader("전체 형법범죄 (연도별 막대그래프)")
        for crime in 전체_형법범죄:
            chart_data = df_long[df_long["범죄유형"] == crime]
            fig = px.bar(chart_data, x="연도", y="범죄율", title=crime,
                         labels={"연도": "Year", "범죄율": "Crime Rate"})
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    # ---------------- TAB 2 ----------------
    with tab2:
        st.subheader("주요형법범죄 다중 비교")
        selected_crimes = st.multiselect("✅ 비교할 주요 범죄 유형 선택", 주요_범죄들, default=주요_범죄들[:3])

        if selected_crimes:
            filtered = df_long[df_long["범죄유형"].isin(selected_crimes)]
            fig2 = px.line(filtered, x="연도", y="범죄율", color="범죄유형",
                           title="선택한 주요 형법범죄 연도별 추이",
                           labels={"연도": "Year", "범죄율": "Crime Rate"})
            fig2.update_layout(legend_title_text="범죄 유형")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("⛔ 하나 이상의 주요 범죄 유형을 선택해주세요.")
else:
    st.info("👆 왼쪽에서 Excel 파일을 업로드해주세요.")
