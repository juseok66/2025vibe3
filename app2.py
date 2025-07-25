import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="서울시 인구 피라미드", layout="wide")
st.title("👥 서울특별시 남녀 연령별 인구 피라미드 (2025년 6월 기준)")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("남녀구분.csv", encoding="cp949")
    return df

df = load_data()

# 서울특별시 전체 행 추출
seoul_df = df[df["행정구역"].str.contains("서울특별시") & df["행정구역"].str.contains(r"\(")]

if seoul_df.empty:
    st.error("❌ 서울시 전체 인구 데이터를 찾을 수 없습니다.")
    st.stop()

row = seoul_df.iloc[0]

# 남성/여성 컬럼 추출
male_cols = [col for col in df.columns if "2025년06월_남_" in col and "세" in col]
female_cols = [col for col in df.columns if "2025년06월_여_" in col and "세" in col]
ages = [col.split("_")[-1].replace("세", "") for col in male_cols]

# 숫자 변환
male_counts = pd.to_numeric(
    row[male_cols].astype(str).str.replace(",", "").str.strip(),
    errors="coerce"
).fillna(0).astype(int).tolist()

female_counts = pd.to_numeric(
    row[female_cols].astype(str).str.replace(",", "").str.strip(),
    errors="coerce"
).fillna(0).astype(int).tolist()

# 합계 계산
total_counts = [m + f for m, f in zip(male_counts, female_counts)]

# 피라미드 데이터프레임
pyramid_df = pd.DataFrame({
    "연령": ages,
    "남성": [-x for x in male_counts],
    "여성": female_counts,
    "합계": total_counts
})

# 🔹 표 출력
st.markdown("### 📋 연령별 총인구 표")
st.dataframe(
    pyramid_df[["연령", "남성", "여성", "합계"]].sort_values("연령", ascending=False).reset_index(drop=True),
    use_container_width=True
)

# 🔹 피라미드 그래프
pyramid_long = pyramid_df.melt(id_vars="연령", value_vars=["남성", "여성"], var_name="성별", value_name="인구수")
pyramid_long["연령"] = pd.Categorical(pyramid_long["연령"], categories=ages[::-1], ordered=True)

fig = px.bar(
    pyramid_long,
    x="인구수",
    y="연령",
    color="성별",
    orientation="h",
    title="서울특별시 남녀 인구 피라미드 (2025년 6월)",
    color_discrete_map={"남성": "blue", "여성": "pink"},
    height=800
)

st.plotly_chart(fig, use_container_width=True)

# 🔹 총합 선 그래프 (옵션)
st.markdown("### 📈 연령별 총인구 선 그래프")
fig_total = px.line(
    pyramid_df,
    x="연령",
    y="합계",
    title="연령별 총 인구수 추이 (남+여)",
    markers=True
)
st.plotly_chart(fig_total, use_container_width=True)
