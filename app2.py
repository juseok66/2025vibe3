import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("남녀구분.csv", encoding="cp949")

df = load_data()

st.set_page_config(page_title="서울시 인구 피라미드", layout="wide")
st.title("👥 서울시 남녀 연령별 인구 피라미드 (2025년 6월 기준)")

# 서울특별시 전체 인구 데이터를 포함한 행 찾기
seoul_df = df[df["행정구역"].str.contains("서울특별시") & df["행정구역"].str.contains("\(")]

if seoul_df.empty:
    st.error("서울시 전체 데이터가 존재하지 않습니다.")
    st.stop()

# 첫 번째 행 사용
row = seoul_df.iloc[0]

# 남성/여성 컬럼
male_cols = [col for col in df.columns if "2025년06월_남_" in col and "세" in col]
female_cols = [col for col in df.columns if "2025년06월_여_" in col and "세" in col]

ages = [col.split("_")[-1].replace("세", "") for col in male_cols]
male_counts = row[male_cols].str.replace(",", "").astype(int).tolist()
female_counts = row[female_cols].str.replace(",", "").astype(int).tolist()

# 데이터 프레임 구성
pyramid_df = pd.DataFrame({
    "연령": ages,
    "남성": [-x for x in male_counts],
    "여성": female_counts
})

# Long-form 변환
pyramid_long = pyramid_df.melt(id_vars="연령", var_name="성별", value_name="인구수")
pyramid_long["연령"] = pd.Categorical(pyramid_long["연령"], categories=ages[::-1], ordered=True)

# Plotly 그리기
fig = px.bar(
    pyramid_long,
    x="인구수",
    y="연령",
    color="성별",
    orientation="h",
    title="서울특별시 남녀 인구 피라미드",
    color_discrete_map={"남성": "blue", "여성": "pink"},
    height=800
)

st.plotly_chart(fig, use_container_width=True)
