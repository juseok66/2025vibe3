import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("남녀구분.csv", encoding="cp949")
    return df

df = load_data()

st.set_page_config(page_title="서울시 인구 피라미드", layout="wide")
st.title("👥 서울시 남녀 연령별 인구 피라미드 (2025년 6월 기준)")

# 서울시 전체 데이터만 추출
seoul_df = df[df["행정구역"].str.startswith("서울특별시 ") & (df["행정구역"].str.count(" ") == 1)]

# 남성/여성 연령별 컬럼 찾기
male_cols = [col for col in seoul_df.columns if "2025년06월_남_" in col and "세" in col]
female_cols = [col for col in seoul_df.columns if "2025년06월_여_" in col and "세" in col]

# 연령 레이블 추출
ages = [col.split("_")[-1].replace("세", "") for col in male_cols]
male_counts = seoul_df.iloc[0][male_cols].str.replace(",", "").astype(int).tolist()
female_counts = seoul_df.iloc[0][female_cols].str.replace(",", "").astype(int).tolist()

# 데이터프레임 구성
pyramid_df = pd.DataFrame({
    "연령": ages,
    "남성": [-x for x in male_counts],  # 음수로 표시 (왼쪽)
    "여성": female_counts
})

# Long-form으로 변환
pyramid_long = pyramid_df.melt(id_vars="연령", var_name="성별", value_name="인구수")
pyramid_long["연령"] = pd.Categorical(pyramid_long["연령"], categories=ages[::-1], ordered=True)

# Plotly 시각화
fig = px.bar(
    pyramid_long,
    x="인구수",
    y="연령",
    color="성별",
    orientation="h",
    title="서울특별시 전체 남녀 연령별 인구 피라미드 (2025년 6월)",
    color_discrete_map={"남성": "blue", "여성": "pink"},
    height=800
)

st.plotly_chart(fig, use_container_width=True)
