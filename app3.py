import pandas as pd
import plotly.express as px

# 전처리 및 컬럼명 설정 (이미 수행되었다고 가정)
범죄대분류 = "죄종별(1)죄종별(1)"
범죄소분류 = "죄종별(2)죄종별(2)"

df_clean = df_raw.iloc[2:].copy()
df_clean.columns = columns

# 살인기수 & 2022년도 필터링
df_filtered = df_clean[df_clean[범죄소분류] == "살인기수"]
year_cols = [col for col in df_filtered.columns if col.startswith("2022")]
df_2022 = df_filtered[[범죄대분류, 범죄소분류] + year_cols]

# 긴 형태로 변환
df_melted = df_2022.melt(id_vars=[범죄대분류, 범죄소분류], var_name="구분", value_name="인원수")
df_melted["성별"] = df_melted["구분"].str.extract(r"(남자|여자)")
df_melted["연령대"] = df_melted["구분"].str.replace("2022", "").str.replace("남자", "").str.replace("여자", "").str.strip()

# 수치형 변환 및 NaN 제거
df_melted["인원수"] = pd.to_numeric(df_melted["인원수"].astype(str).str.replace(",", "").replace("-", "0"), errors="coerce")
df_melted.dropna(subset=["성별", "연령대", "인원수"], inplace=True)

# Plotly 시각화
fig = px.bar(df_melted, x="연령대", y="인원수", color="성별",
             title="2022년 살인기수 범죄자 성별/연령대 분포",
             labels={"연령대": "연령대", "인원수": "명", "성별": "성별"})
fig.update_layout(xaxis_tickangle=-45)
fig.show()
