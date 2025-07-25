import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 범죄율 분석 대시보드")

uploaded_file = st.file_uploader("📁 범죄율 Excel 파일 업로드 (.xlsx)", type=["xlsx"])

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file, sheet_name=0)

    # ✅ NaN 셀 병합처럼 위의 값으로 채움
    df_raw["Unnamed: 0"] = df_raw["Unnamed: 0"].fillna(method="ffill")

    # ✅ 범죄유형 생성 (예: "주요 형법범죄_살인")
    df_raw["범죄유형"] = df_raw["Unnamed: 0"].str.strip() + "_" + df_raw["Unnamed: 1"].fillna("").str.strip()

    # ✅ 불필요 열 제거 후 전치
    df = df_raw.drop(columns=["Unnamed: 0", "Unnamed: 1"], errors="ignore")
    df = df.set_index("범죄유형").T
    df.index.name = "연도"

    # ✅ 값 정제 (숫자형 변환)
    df = df.applymap(lambda x: str(x).replace(",", "").replace("-", "").replace("없음", "").strip())
    df = df.apply(pd.to_numeric, errors="coerce")

    # ✅ 긴 형태로 변환
    df_long = df.reset_index().melt(id_vars="연도", var_name="범죄유형", value_name="범죄율")

    # ✅ 유형 분리
    전체형법 = [c for c in df.columns if "전체" in c]
    주요형법 = [c for c in df.columns if "주요" in c and "전체" not in c]

    tab1, tab2 = st.tabs(["📌 전체 형법범죄", "📌 주요형법범죄 비교"])

    # ---------------- TAB 1 ----------------
    with tab1:
        st.subheader("전체 형법범죄 연도별 변화")
        for crime in 전체형법:
            sub_df = df_long[df_long["범죄유형"] == crime]
            fig = px.bar(sub_df, x="연도", y="범죄율", title=f"📌 {crime}",
                         labels={"연도": "Year", "범죄율": "Crime Rate"})
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    # ---------------- TAB 2 ----------------
    with tab2:
        st.subheader("주요 형법범죄 비교")
        options = st.multiselect("✅ 비교할 범죄 선택", 주요형법, default=주요형법[:3])
        if options:
            sub_df = df_long[df_long["범죄유형"].isin(options)]
            fig2 = px.line(sub_df, x="연도", y="범죄율", color="범죄유형",
                           title="주요 범죄 비교 (연도별 추이)",
                           labels={"연도": "Year", "범죄율": "Crime Rate"})
            fig2.update_layout(legend_title="범죄유형")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("⛔ 하나 이상의 범죄를 선택해주세요.")
else:
    st.info("👆 왼쪽에서 Excel 파일을 업로드해주세요.")
