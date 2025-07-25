import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="형법범죄 통계 시각화", layout="wide")
st.title("📉 형법범죄 통계 분석 대시보드")

# ---------------- 파일 업로드 ----------------
st.sidebar.header("📂 데이터 파일 업로드")
uploaded_crime = st.sidebar.file_uploader("형법범죄 통계 엑셀 파일", type=["xlsx"], key="crime")

# ---------------- 메인 탭 ----------------
tab = st.container()

with tab:
    st.header("📊 형법범죄 연도별 추이 분석")

    if uploaded_crime:
        try:
            df_crime_raw = pd.read_excel(uploaded_crime, sheet_name=0, header=None)

            # 컬럼명 설정 및 정리
            df_crime_raw.columns.values[0:2] = ["범죄분류", "범죄유형"]
            df_crime_raw.columns = df_crime_raw.columns.astype(str).str.strip()
            df_crime_raw["범죄유형"] = df_crime_raw["범죄유형"].fillna(method="ffill")

            # 데이터 변환
            df_crime = df_crime_raw.melt(id_vars=["범죄분류", "범죄유형"], var_name="연도", value_name="범죄율")
            df_crime["연도"] = pd.to_numeric(df_crime["연도"], errors="coerce")
            df_crime = df_crime.dropna(subset=["연도", "범죄율"])
            df_crime["범죄율"] = pd.to_numeric(df_crime["범죄율"].astype(str).str.replace(",", "").replace("-", "0"), errors="coerce")

            st.subheader("🔍 데이터 미리보기")
            st.dataframe(df_crime.head(10))

            # 범죄유형 선택
            범죄유형_list = sorted(df_crime["범죄유형"].unique())
            selected_types = st.multiselect("📌 분석할 범죄유형을 선택하세요", 범죄유형_list, default=범죄유형_list[:3])

            # 연도 범위 슬라이더
            min_year, max_year = int(df_crime["연도"].min()), int(df_crime["연도"].max())
            year_range = st.slider("📆 연도 범위 선택", min_value=min_year, max_value=max_year, value=(min_year, max_year))

            # 필터링
            df_filtered = df_crime[
                (df_crime["범죄유형"].isin(selected_types)) &
                (df_crime["연도"] >= year_range[0]) & (df_crime["연도"] <= year_range[1])
            ]

            # 시각화
            st.subheader("📈 범죄유형별 연도별 범죄율 추이")
            fig = px.line(df_filtered, x="연도", y="범죄율", color="범죄유형", markers=True)
            fig.update_layout(yaxis_title="범죄율 (인구 10만 명당)", xaxis_title="연도")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error("❌ 오류 발생:")
            st.exception(e)
    else:
        st.info("⬆️ 좌측에서 형법범죄 통계 엑셀 파일을 업로드하세요.")
