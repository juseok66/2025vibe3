import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="전국 인구 피라미드", layout="wide")
st.title("👥 전국 시도별 남녀 연령별 인구 피라미드 (2025년 6월 기준)")

# CSV 파일 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("남녀구분.csv", encoding="cp949")

df = load_data()

# 시도명 추출
df["시도"] = df["행정구역"].str.extract(r'^(.*?[시도])')
sido_list = df["시도"].dropna().unique().tolist()

# 시도별 탭 생성
tabs = st.tabs(sido_list)

for i, sido in enumerate(sido_list):
    with tabs[i]:
        st.subheader(f"📍 {sido} 인구 피라미드")

        # 시도 전체 인구 합계 행 필터
        target_df = df[df["행정구역"].str.startswith(sido) & df["행정구역"].str.contains(r"\(")]
        if target_df.empty:
            st.warning(f"{sido} 인구 데이터가 존재하지 않습니다.")
            continue

        row = target_df.iloc[0]

        # 남성/여성 연령별 컬럼 찾기
        male_cols = [col for col in df.columns if "2025년06월_남_" in col and "세" in col]
        female_cols = [col for col in df.columns if "2025년06월_여_" in col and "세" in col]
        ages = [col.split("_")[-1].replace("세", "") for col in male_cols]

        # 인구수 숫자 변환
        male_counts = pd.to_numeric(
            row[male_cols].astype(str).str.replace(",", "").str.strip(),
            errors="coerce"
        ).fillna(0).astype(int).tolist()

        female_counts = pd.to_numeric(
            row[female_cols].astype(str).str.replace(",", "").str.strip(),
            errors="coerce"
        ).fillna(0).astype(int).tolist()

        total_counts = [m + f for m, f in zip(male_counts, female_counts)]

        # 데이터프레임 구성
        pyramid_df = pd.DataFrame({
            "연령": ages,
            "남성": [-x for x in male_counts],
            "여성": female_counts,
            "합계": total_counts
        })
        pyramid_df["연령"] = pd.Categorical(pyramid_df["연령"], categories=ages[::-1], ordered=True)

        # 피라미드 그래프
        pyramid_long = pyramid_df.melt(id_vars="연령", value_vars=["남성", "여성"], var_name="성별", value_name="인구수")
        fig1 = px.bar(
            pyramid_long,
            x="인구수",
            y="연령",
            color="성별",
            orientation="h",
            title=f"{sido} 남녀 인구 피라미드",
            color_discrete_map={"남성": "blue", "여성": "pink"},
            height=800
        )
        st.plotly_chart(fig1, use_container_width=True)

        # 총 인구수 세로 막대 그래프
        st.markdown(f"### 📊 {sido} 연령별 총 인구수 (세로 막대 그래프)")
        total_df = pyramid_df[["연령", "합계"]].sort_values("연령")

        fig2 = px.bar(
            total_df,
            x="연령",
            y="합계",
            title=f"{sido} 연령별 총 인구수 (남 + 여)",
            color_discrete_sequence=["gray"],
            height=500
        )
        st.plotly_chart(fig2, use_container_width=True)
